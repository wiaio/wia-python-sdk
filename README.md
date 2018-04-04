# Wia SDK for Python
[![Build Status](https://travis-ci.org/wiaio/wia-python-sdk.svg?branch=master)](https://travis-ci.org/wiaio/wia-python-sdk)
[![Coverage Status](https://coveralls.io/repos/github/wiaio/wia-python-sdk/badge.svg?branch=master)](https://coveralls.io/github/wiaio/wia-python-sdk?branch=master)

## Documentation
For full documentation visit [http://docs.wia.io/](http://docs.wia.io/)

## Installation
You will need to have `pip` already installed on your machine. Then run the command:
```
pip install wia
```

## Usage
Import the Wia library
```python
from wia import Wia
```

Create an instance of Wia
```python
wia = Wia()
```

Example code
```python
from wia import Wia

wia = Wia()
wia.access_token = "your-access-token"

wia.Event.publish(name="Test Event", data=21)
```

## License
This SDK is distributed under the MIT License

Copyright (c) 2010-2018 Wia Technologies Limited. https://wia.io

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
