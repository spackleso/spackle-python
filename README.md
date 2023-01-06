# Spackle Python Library

[![CI](https://github.com/spackleso/spackle-python/actions/workflows/test.yml/badge.svg)](https://github.com/spackleso/spackle-python/actions/workflows/test.yml)

The Spackle Python library provides optimized access to billing aware flags created on the Spackle platform.

## Documentation

See the [Python API docs](https://docs.spackle.so/python).

## Setup

### Install the Spackle library

```
pip install spackle-python
```

### Configure your environment
In order to use Spackle, you need to configure your API key on the `spackle` module. You can find your API key in Spackle app [settings page](https://dashboard.stripe.com/settings/apps/so.spackle.stripe).

```
import spackle
spackle.api_key = "<api key>"
```

## Usage

### Fetch a customer

Spackle uses stripe ids as references to customer features.

```
customer = spackle.Customer.retrive("cus_00000000")
```

### Verify feature access

```
customer.enabled('feature_key')
```

### Fetch a feature limit

```
customer.limit('feature_key')
```