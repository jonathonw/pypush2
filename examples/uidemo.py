#!/usr/bin/env python

import pypush2.ui

myUiSpec = [
  {
    "title": "Tab 1",
    "id": "tab1",
    "actions": [
      {
        "title": "Action 1",
        "id": "tab1action1"
      },
      {
        "title": "Action 2",
        "id": "tab1action2"
      }
    ],
    "encoders": [
      {
        "title": "Encoder 1",
        "id": "tab1encoder1",
        "value": 2.3,
        "min": 0.0,
        "max": 5.0
      },
      {
        "title": "Encoder 2",
        "id": "tab1encoder2",
        "value": 3.8,
        "min": 0.0,
        "max": 5.0
      }
    ]
  },
  {
    "title": "Tab 2",
    "id": "tab2",
    "actions": [
      {
        "title": "Action 3",
        "id": "tab2action3"
      },
      {
        "title": "Action 4",
        "id": "tab2action4"
      }
    ],
    "encoders": [
      {
        "title": "Encoder 1",
        "id": "tab2encoder1",
        "value": 0.3,
        "min": 0.0,
        "max": 5.0
      },
      {
        "title": "Encoder 2",
        "id": "tab2encoder2",
        "value": 5.0,
        "min": 0.0,
        "max": 5.0
      }
    ]
  }
]

def main():
  pushUi = pypush2.ui.PushUi(myUiSpec)
  pushUi.run()

if __name__ == "__main__":
  main()
