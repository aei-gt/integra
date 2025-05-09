app_name = "integra"
app_title = "INTEGRA"
app_publisher = "AEI"
app_description = "Integración de Personalizaciones ERPNext"
app_email = "info@aei.gt"
app_license = "mit"
# required_apps = []

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/integra/css/integra.css"
# app_include_js = "/assets/integra/js/manu.js"

# include js, css files in header of web template
# web_include_css = "/assets/integra/css/integra.css"
# web_include_js = "/assets/integra/js/integra.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "integra/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {"Salary Structure Assignment" : "public/js/salary_structure_assignment.js",
              "Employee" : "public/js/employee.js",
              "Issue" : "public/js/issue.js",
              "Sales Invoice" : "public/js/custom_si.js",
              "Salary Slip" : "public/js/custom_salary_slp.js"}
# doctype_js = {"Employee" : "public/js/employee.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "integra/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "integra.utils.jinja_methods",
# 	"filters": "integra.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "integra.install.before_install"
# after_install = "integra.manu.hide_manu"

# Uninstallation
# ------------

# before_uninstall = "integra.uninstall.before_uninstall"
# after_uninstall = "integra.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "integra.utils.before_app_install"
# after_app_install = "integra.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "integra.utils.before_app_uninstall"
# after_app_uninstall = "integra.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "integra.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# before_migrate = "integra.manu.hide_manu"
# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Employee": {
		"validate": "integra.events.validator.validator",
    },
    "Issue": {
		"after_insert": "integra.events.api.send_new_client_whatsapp_message",
        "on_update": "integra.events.api.send_updated_whatsapp_message",
    },
    "Sales Invoice": {
        "validate": "integra.events.custom_si.validate_item_types"
    }
}

# Scheduled Tasks
# ---------------
scheduler_events = {
    "hourly": [
        "integra.hikvision.hikvision.fetch_hik_vision_records"
    ],
    "cron": {
        "*/10 * * * *": [
            "integra.hikvision.hikvision.fetch_hik_vision_records"
        ],
    }
}






# scheduler_events = {
# 	"all": [
# 		"integra.tasks.all"
# 	],
# 	"daily": [
# 		"integra.tasks.daily"
# 	],
# 	"hourly": [
# 		"integra.tasks.hourly"
# 	],
# 	"weekly": [
# 		"integra.tasks.weekly"
# 	],
# 	"monthly": [
# 		"integra.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "integra.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "integra.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "integra.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["integra.utils.before_request"]
# after_request = ["integra.utils.after_request"]

# Job Events
# ----------
# before_job = ["integra.utils.before_job"]
# after_job = ["integra.utils.after_job"]

# User Data Protection
# --------------------
# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"integra.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

# fixtures = ["Workflow","Workflow State"]
fixtures = [
    {
        "dt": "Custom Field",
        "filters": [
            [
                "name",
                "in",
                [
                    "Salary Slip-custom_deduccion_total",
                    "Salary Slip-custom_pago_neto"
                ],
            ]
        ],
    },
]