from applications.common.admin import register_app_models
from applications.matches.apps import MatchesConfig


register_app_models(app_name=MatchesConfig.name)