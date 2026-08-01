def create_card(base_url):

    return {


        "name":
        "Invoice Action Agent",


        "description":
        "AI agent that reconciles invoice packages",


        "version":
        "1.0",



        "capabilities":{

            "streaming":False,

            "pushNotifications":False

        },


        "skills":[

            {

            "name":
            "invoice_action_agent",


            "description":
            "Invoice decision and evidence extraction agent",


            "tags":[
                "invoice",
                "audit",
                "finance"
            ]

            }

        ],



        "supportedInterfaces":[

            {

            "url":
            base_url,


            "protocolBinding":
            "HTTP+JSON",


            "protocolVersion":
            "1.0"

            }

        ],



        "defaultInputModes":[

            "application/vnd.ga5.invoice-claim-batch+json"

        ],



        "defaultOutputModes":[

            "application/vnd.ga5.invoice-action-proposals+json",

            "application/vnd.ga5.invoice-action-receipts+json"

        ]

    }