# from django.conf import settings
import os
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.v18.services.types.keyword_plan_idea_service import (
    GenerateKeywordIdeaResponse,
    GenerateKeywordIdeasRequest,
)

# from apps.core.choices import CountryChoices

# Simple settings and choices replacement for standalone usage
class settings:
    GOOGLE_ADS_YAML_FILE = os.path.join(os.path.dirname(__file__), '..', 'keys', 'google-ads.yaml')

class CountryChoices:
    values = ["2840", "2036", "2826", "2124", "2250", "2276", "2380", "2392", "2484", "2528"]
    choices = [
        ("2840", "United States"),
        ("2036", "Canada"), 
        ("2826", "United Kingdom"),
        ("2124", "Germany"),
        ("2250", "France"),
        ("2276", "Italy"),
        ("2380", "Spain"),
        ("2392", "Japan"),
        ("2484", "Australia"),
        ("2528", "Netherlands")
    ]


class GoogleKeywordIdeaGenerator:
    def __init__(
        self,
        location_id: str = "2840",  # Default to US
        keywords: list[str] | str | None = None,
        url: str | None = None,
    ):
        # Initialize client
        self.__client = GoogleAdsClient.load_from_storage(
            getattr(settings, "GOOGLE_ADS_YAML_FILE"), version="v18"
        )
        
        self.page_size = 20
        self.next_page_token = None
        
        # Validate inputs
        if (keywords is None and url is None) or (keywords == "" and url == ""):
            raise ValueError("keywords and url: At least one of them is required")
        
        # Set default location if empty
        if not location_id:
            location_id = "2840"
            
        if location_id not in CountryChoices.values:
            raise ValueError(
                f"location_id should be from following items: {CountryChoices.choices}"
            )
        self.location_id = location_id
        
        # Process keywords
        if isinstance(keywords, list):
            self.keywords = [k.strip() for k in keywords if k.strip()]
        elif isinstance(keywords, str):
            self.keywords = [k.strip() for k in keywords.split(",") if k.strip()]
        else:
            self.keywords = None
            
        # Ensure we have at least one keyword if no URL
        if self.keywords and not any(self.keywords):
            self.keywords = None
            
        self.url = url if url and url.strip() else None

    def set_page_size(self, number: int):
        self.page_size = number

    def set_page_token(self, token: str):
        self.page_token = token

    def set_client_yaml_path(self, path: str):
        self.__client = GoogleAdsClient.load_from_storage(path, version="v18")

    def __configure_request(self):
        language_rn = self.__client.get_service(
            "GoogleAdsService"
        ).language_constant_path(1000)

        keyword_plan_network = (
            self.__client.enums.KeywordPlanNetworkEnum.GOOGLE_SEARCH  # type: ignore
        )

        request: GenerateKeywordIdeasRequest = self.__client.get_type(
            "GenerateKeywordIdeasRequest"
        )  # type: ignore
        request.language = language_rn
        request.page_size = self.page_size
        request.page_token = getattr(self, "next_page_token", None)  # type: ignore
        if self.location_id:
            request.geo_target_constants.append(
                f"geoTargetConstants/{self.location_id}"
            )
        request.customer_id = "6382620946"
        request.include_adult_keywords = False
        request.keyword_plan_network = keyword_plan_network
        request.historical_metrics_options.include_average_cpc = True

        if self.url and not self.keywords:
            request.url_seed.url = self.url
        if self.keywords and not self.url:
            request.keyword_seed.keywords.extend(self.keywords)
        if self.keywords and self.url:
            request.keyword_and_url_seed.url = self.url
            request.keyword_and_url_seed.keywords.extend(self.keywords)
        return request

    def __generate_keyword_ideas(self):
        keyword_plan_idea_service = self.__client.get_service("KeywordPlanIdeaService")
        request = self.__configure_request()
        keyword_ideas: GenerateKeywordIdeaResponse = (
            keyword_plan_idea_service.generate_keyword_ideas(request=request)
        )
        response = keyword_ideas.results
        next_page_token = getattr(keyword_ideas, "next_page_token", None)
        return response, next_page_token

    def get_results(self):
        self.response, self.next_page_token = self.__generate_keyword_ideas()
        self.results = []
        for item in self.response:
            self.results.append(self.__get_metric(item))
        return self.results

    def __get_metric(self, item):
        metrics = item.keyword_idea_metrics
        competition_value = metrics.competition
        metric = {
            "text": item.text,
            "competition": competition_value,
            "low_top_of_page_bid_cpc": int(
                getattr(metrics, "low_top_of_page_bid_micros", 0)
            )
            / 1000000,
            "high_top_of_page_bid_cpc": int(
                getattr(metrics, "high_top_of_page_bid_micros", 0)
            )
            / 1000000,
            "average_cpc": int(getattr(metrics, "average_cpc_micros", 0)) / 1000000,
            "avg_month_searches": item.keyword_idea_metrics.avg_monthly_searches,
        }
        return metric
