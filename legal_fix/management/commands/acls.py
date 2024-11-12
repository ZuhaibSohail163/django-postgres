import json

acls = {
    "subscribers": json.dumps({
      "acl_rules": [
          {
              "roles": [
                  "subscriberUsers.manager"
              ],
              "identity": {
                  "kind": "user",
                  "uid": "{subscriber_id}"
              }
          }
      ]
    }),
    "legal_matters": json.dumps({
        "acl_rules": [
            {
                "roles": [
                    "legalMatters.owner"
                ],
                "identity": {
                    "kind": "user",
                    "uid": "{subscriber_id}"
                }
            },
            {
                "roles": [
                    "legalMatters.viewer"
                ],
                "identity": {
                    "kind": "group",
                    "uid": "{group_id}"
                }
            },
            {
                "roles": [
                    "legalMatters.manager"
                ],
                "identity": {
                    "kind": "user",
                    "uid": "{lawyer_id}"
                }
            }
        ]
    }),
    "documents": json.dumps({
        "acl_rules": [
            {
                "roles": [
                    "documents.viewer"
                ],
                "identity": {
                    "kind": "group",
                    "uid": "{group_id}"
                }
            },
            {
                "roles": [
                    "documents.viewer"
                ],
                "identity": {
                    "kind": "user",
                    "uid": "{subscriber_id}"
                }
            },
            {
                "roles": [
                    "documents.manager"
                ],
                "identity": {
                    "kind": "user",
                    "uid": "{lawyer_id}"
                }
            }
        ]
    }),
    "tasks": json.dumps({
        "acl_rules": [
            {
                "roles": [
                    "tasks.collaborator"
                ],
                "identity": {
                    "kind": "user",
                    "uid": "{lawyer_id}"
                }
            },
            {
                "roles": [
                    "tasks.manager"
                ],
                "identity": {
                    "kind": "user",
                    "uid": "{subscriber_id}"
                }
            },
            {
                "roles": [
                    "tasks.viewer"
                ],
                "identity": {
                    "kind": "group",
                    "uid": "{group_id}"
                }
            }
        ]
    }),
    "notes": json.dumps({
        "acl_rules": [
            {
                "roles": [
                    "notes.manager"
                ],
                "identity": {
                    "kind": "user",
                    "uid": "{lawyer_id}"
                }
            },
            {
                "roles": [
                    "notes.viewer"
                ],
                "identity": {
                    "kind": "group",
                    "uid": "{group_id}"
                }
            }
        ]
    }),
    "calendar_events": json.dumps({
        "acl_rules": [
            {
                "roles": [
                    "calendarEvents.viewer"
                ],
                "identity": {
                    "kind": "user",
                    "uid": "{subscriber_id}"
                }
            },
            {
                "roles": [
                    "calendarEvents.viewer"
                ],
                "identity": {
                    "kind": "user",
                    "uid": "{lawyer_id}"
                }
            },
            {
                "roles": [
                    "calendarEvents.viewer"
                ],
                "identity": {
                    "kind": "group",
                    "uid": "{group_id}"
                }
            }
        ]
    })
}
