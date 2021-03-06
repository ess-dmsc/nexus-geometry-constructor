import json
from typing import Dict

import pytest


@pytest.fixture(scope="function")
def off_pixel_mapping() -> Dict:
    off_shape = """
    {
                  "name": "shape",
                  "attributes": [
                    {
                      "name": "NX_class",
                      "type": "string",
                      "values": "NXoff_geometry"
                    }
                  ],
                  "type": "group",
                  "children": [
                    {
                      "name": "winding_order",
                      "type": "dataset",
                      "values": [
                        1,
                        0,
                        4,
                        4,
                        0,
                        3,
                        3,
                        0,
                        2,
                        2,
                        0,
                        1,
                        1,
                        5,
                        2,
                        2,
                        5,
                        3,
                        3,
                        5,
                        4,
                        4,
                        5,
                        1
                      ]
                    },
                    {
                      "name": "faces",
                      "type": "dataset",
                      "values": [
                        0,
                        3,
                        6,
                        9,
                        12,
                        15,
                        18,
                        21
                      ]
                    },
                    {
                      "name": "vertices",
                      "attributes": [
                        {
                          "name": "units",
                          "type": "string",
                          "values": "m"
                        }
                      ],
                      "type": "dataset",
                      "values": [
                        [
                          0.0,
                          0.0,
                          1.0
                        ],
                        [
                          1.0,
                          0.0,
                          0.0
                        ],
                        [
                          0.0,
                          1.0,
                          0.0
                        ],
                        [
                          -1.0,
                          0.0,
                          0.0
                        ],
                        [
                          0.0,
                          -1.0,
                          0.0
                        ],
                        [
                          0.0,
                          0.0,
                          -1.0
                        ]
                      ]
                    },
                    {
                      "name": "detector_faces",
                      "type": "dataset",
                      "values": [
                        [
                          0,
                          2
                        ],
                        [
                          1,
                          3
                        ],
                        [
                          2,
                          4
                        ],
                        [
                          3,
                          5
                        ],
                        [
                          4,
                          6
                        ],
                        [
                          5,
                          7
                        ],
                        [
                          6,
                          8
                        ],
                        [
                          7,
                          9
                        ]
                      ]
                    }
                  ]
                }
    """
    return json.loads(off_shape)


@pytest.fixture(scope="function")
def off_shape_json() -> Dict:
    """
    Mesh for a simple unit cube, centred at 0, 0, 0
    """
    off_shape = """
    {
      "type":"group",
      "name":"shape",
      "children":[
        {
          "type":"dataset",
          "name":"faces",
          "dataset":{
            "type":"int32",
            "size":[
              6
            ]
          },
          "values":[
            0,
            4,
            8,
            12,
            16,
            20
          ]
        },
        {
          "type":"dataset",
          "name":"vertices",
          "dataset":{
            "type":"float",
            "size":[
              8,
              3
            ]
          },
          "values":[
            [
              -0.5,
              -0.5,
              0.5
            ],
            [
              0.5,
              -0.5,
              0.5
            ],
            [
              -0.5,
              0.5,
              0.5
            ],
            [
              0.5,
              0.5,
              0.5
            ],
            [
              -0.5,
              0.5,
              -0.5
            ],
            [
              0.5,
              0.5,
              -0.5
            ],
            [
              -0.5,
              -0.5,
              -0.5
            ],
            [
              0.5,
              -0.5,
              -0.5
            ]
          ],
          "attributes":[
            {
              "name":"units",
              "values":"m"
            }
          ]
        },
        {
          "type":"dataset",
          "name":"winding_order",
          "dataset":{
            "type":"int32",
            "size":[
              24
            ]
          },
          "values":[
            0,
            1,
            3,
            2,
            2,
            3,
            5,
            4,
            4,
            5,
            7,
            6,
            6,
            7,
            1,
            0,
            1,
            7,
            5,
            3,
            6,
            0,
            2,
            4
          ]
        }
      ],
      "attributes":[
        {
          "name":"NX_class",
          "values":"NXoff_geometry"
        }
      ]
    }
    """
    return json.loads(off_shape)


@pytest.fixture(scope="function")
def cylindrical_shape_json() -> dict:
    cylindrical_shape = """
    {
      "type":"group",
      "name":"pixel_shape",
      "children":[
        {
          "type":"dataset",
          "name":"cylinders",
          "dataset":{
            "type":"int32",
            "size":[
              1,
              3
            ]
          },
          "values":[
            [
              0,
              1,
              2
            ]
          ]
        },
        {
          "type":"dataset",
          "name":"vertices",
          "dataset":{
            "type":"double",
            "size":[
              3,
              3
            ]
          },
          "values":[
            [
              -0.01,
              0,
              0
            ],
            [
              -0.01,
              0.009,
              0
            ],
            [
              0.01,
              0,
              0
            ]
          ],
          "attributes":[
            {
              "name":"units",
              "values":"m"
            }
          ]
        }
      ],
      "attributes":[
        {
          "name":"NX_class",
          "values":"NXcylindrical_geometry"
        }
      ]
    }
    """
    return json.loads(cylindrical_shape)


@pytest.fixture(scope="function")
def pixel_grid_list() -> list:
    children_list = """
    [
      {
        "type": "dataset",
        "name": "detector_number",
        "dataset": {
          "type": "int32",
          "size": [
            100
          ]
        },
        "values": [
          2100000,
          2100001,
          2100002,
          2100003,
          2100004,
          2100005,
          2100006,
          2100007,
          2100008,
          2100009,
          2102000,
          2102001,
          2102002,
          2102003,
          2102004,
          2102005,
          2102006,
          2102007,
          2102008,
          2102009,
          2104000,
          2104001,
          2104002,
          2104003,
          2104004,
          2104005,
          2104006,
          2104007,
          2104008,
          2104009,
          2106000,
          2106001,
          2106002,
          2106003,
          2106004,
          2106005,
          2106006,
          2106007,
          2106008,
          2106009,
          2108000,
          2108001,
          2108002,
          2108003,
          2108004,
          2108005,
          2108006,
          2108007,
          2108008,
          2108009,
          2101000,
          2101001,
          2101002,
          2101003,
          2101004,
          2101005,
          2101006,
          2101007,
          2101008,
          2101009,
          2103000,
          2103001,
          2103002,
          2103003,
          2103004,
          2103005,
          2103006,
          2103007,
          2103008,
          2103009,
          2105000,
          2105001,
          2105002,
          2105003,
          2105004,
          2105005,
          2105006,
          2105007,
          2105008,
          2105009,
          2107000,
          2107001,
          2107002,
          2107003,
          2107004,
          2107005,
          2107006,
          2107007,
          2107008,
          2107009,
          2109000,
          2109001,
          2109002,
          2109003,
          2109004,
          2109005,
          2109006,
          2109007,
          2109008,
          2109009
        ]
      },
      {
        "type": "dataset",
        "name": "x_pixel_offset",
        "dataset": {
          "type": "double",
          "size": [
            100
          ]
        },
        "values": [
          -0.12,
          -0.09777777777777777,
          -0.07555555555555554,
          -0.05333333333333333,
          -0.031111111111111103,
          -0.008888888888888877,
          0.013333333333333336,
          0.03555555555555556,
          0.05777777777777779,
          0.08,
          -0.12,
          -0.09777777777777777,
          -0.07555555555555554,
          -0.05333333333333333,
          -0.031111111111111103,
          -0.008888888888888877,
          0.013333333333333336,
          0.03555555555555556,
          0.05777777777777779,
          0.08,
          -0.12,
          -0.09777777777777777,
          -0.07555555555555554,
          -0.05333333333333333,
          -0.031111111111111103,
          -0.008888888888888877,
          0.013333333333333336,
          0.03555555555555556,
          0.05777777777777779,
          0.08,
          -0.12,
          -0.09777777777777777,
          -0.07555555555555554,
          -0.05333333333333333,
          -0.031111111111111103,
          -0.008888888888888877,
          0.013333333333333336,
          0.03555555555555556,
          0.05777777777777779,
          0.08,
          -0.12,
          -0.09777777777777777,
          -0.07555555555555554,
          -0.05333333333333333,
          -0.031111111111111103,
          -0.008888888888888877,
          0.013333333333333336,
          0.03555555555555556,
          0.05777777777777779,
          0.08,
          -0.08,
          -0.057777777777777775,
          -0.035555555555555556,
          -0.013333333333333336,
          0.00888888888888889,
          0.031111111111111117,
          0.05333333333333333,
          0.07555555555555556,
          0.09777777777777778,
          0.12,
          -0.08,
          -0.057777777777777775,
          -0.035555555555555556,
          -0.013333333333333336,
          0.00888888888888889,
          0.031111111111111117,
          0.05333333333333333,
          0.07555555555555556,
          0.09777777777777778,
          0.12,
          -0.08,
          -0.057777777777777775,
          -0.035555555555555556,
          -0.013333333333333336,
          0.00888888888888889,
          0.031111111111111117,
          0.05333333333333333,
          0.07555555555555556,
          0.09777777777777778,
          0.12,
          -0.08,
          -0.057777777777777775,
          -0.035555555555555556,
          -0.013333333333333336,
          0.00888888888888889,
          0.031111111111111117,
          0.05333333333333333,
          0.07555555555555556,
          0.09777777777777778,
          0.12,
          -0.08,
          -0.057777777777777775,
          -0.035555555555555556,
          -0.013333333333333336,
          0.00888888888888889,
          0.031111111111111117,
          0.05333333333333333,
          0.07555555555555556,
          0.09777777777777778,
          0.12
        ],
        "attributes": [
          {
            "name": "units",
            "values": "m"
          }
        ]
      },
      {
        "type": "dataset",
        "name": "y_pixel_offset",
        "dataset": {
          "type": "double",
          "size": [
            100
          ]
        },
        "values": [
          -0.08,
          -0.08,
          -0.08,
          -0.08,
          -0.08,
          -0.08,
          -0.08,
          -0.08,
          -0.08,
          -0.08,
          -0.04,
          -0.04,
          -0.04,
          -0.04,
          -0.04,
          -0.04,
          -0.04,
          -0.04,
          -0.04,
          -0.04,
          0,
          0,
          0,
          0,
          0,
          0,
          0,
          0,
          0,
          0,
          0.039999999999999994,
          0.039999999999999994,
          0.039999999999999994,
          0.039999999999999994,
          0.039999999999999994,
          0.039999999999999994,
          0.039999999999999994,
          0.039999999999999994,
          0.039999999999999994,
          0.039999999999999994,
          0.08,
          0.08,
          0.08,
          0.08,
          0.08,
          0.08,
          0.08,
          0.08,
          0.08,
          0.08,
          -0.1,
          -0.1,
          -0.1,
          -0.1,
          -0.1,
          -0.1,
          -0.1,
          -0.1,
          -0.1,
          -0.1,
          -0.060000000000000005,
          -0.060000000000000005,
          -0.060000000000000005,
          -0.060000000000000005,
          -0.060000000000000005,
          -0.060000000000000005,
          -0.060000000000000005,
          -0.060000000000000005,
          -0.060000000000000005,
          -0.060000000000000005,
          -0.020000000000000004,
          -0.020000000000000004,
          -0.020000000000000004,
          -0.020000000000000004,
          -0.020000000000000004,
          -0.020000000000000004,
          -0.020000000000000004,
          -0.020000000000000004,
          -0.020000000000000004,
          -0.020000000000000004,
          0.01999999999999999,
          0.01999999999999999,
          0.01999999999999999,
          0.01999999999999999,
          0.01999999999999999,
          0.01999999999999999,
          0.01999999999999999,
          0.01999999999999999,
          0.01999999999999999,
          0.01999999999999999,
          0.06,
          0.06,
          0.06,
          0.06,
          0.06,
          0.06,
          0.06,
          0.06,
          0.06,
          0.06
        ],
        "attributes": [
          {
            "name": "units",
            "values": "m"
          }
        ]
      }
    ]
    """
    return json.loads(children_list)
