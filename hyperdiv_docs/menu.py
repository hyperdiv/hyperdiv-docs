from .pages.introduction.overview import overview as introduction_overview
from .pages.introduction.docs_overview import docs_overview

from .pages.guide.getting_started import getting_started
from .pages.guide.components import components as guide_components
from .pages.guide.interactivity import interactivity
from .pages.guide.component_props import component_props
from .pages.guide.layout import layout
from .pages.guide.conditional_rendering import conditional_rendering
from .pages.guide.loops import loops
from .pages.guide.state import state
from .pages.guide.modular_apps import modular_apps
from .pages.guide.tasks import tasks
from .pages.guide.pages_and_navigation import pages_and_navigation
from .pages.guide.using_the_app_template import using_the_app_template
from .pages.guide.static_assets import static_assets
from .pages.guide.deploying import deploying
from .pages.guide.matplotlib_charts import matplotlib_charts

from .pages.reference.components import components
from .pages.reference.env_variables import env_variables
from .pages.reference.design_tokens import design_tokens
from .pages.reference.prop_types import prop_types
from .pages.reference.icons import icons
from .pages.reference.cli import cli

menu = {
    "Introduction": {
        "Hyperdiv Overview": {"href": introduction_overview.path},
        "This Documentation App": {"href": docs_overview.path},
    },
    "Guide": {
        "Getting Started": {"href": getting_started.path},
        "Component Basics": {"href": guide_components.path},
        "Interactivity Basics": {"href": interactivity.path},
        "Component Props": {"href": component_props.path},
        "Style & Layout": {"href": layout.path},
        "Conditional Rendering": {"href": conditional_rendering.path},
        "Rendering in Loops": {"href": loops.path},
        "Custom State": {"href": state.path},
        "Modular Apps": {"href": modular_apps.path},
        "Asynchronous Tasks": {"href": tasks.path},
        "Pages & Navigation": {"href": pages_and_navigation.path},
        "Using The App Template": {"href": using_the_app_template.path},
        "Matplotlib Charts": {"href": matplotlib_charts.path},
        "Static Assets": {"href": static_assets.path},
        "Deploying Hyperdiv": {"href": deploying.path},
    },
    "Reference": {
        "Hyperdiv API": {"href": components.path},
        "Design Tokens": {"href": design_tokens.path},
        "Prop Types": {"href": prop_types.path},
        "Icons": {"href": icons.path},
        "Environment Variables": {"href": env_variables.path},
        "The Hyperdiv CLI": {"href": cli.path},
    },
}
