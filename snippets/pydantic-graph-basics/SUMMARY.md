# Pydantic Graph IP Analysis - Summary

## Purpose

A demonstration of the `pydantic-graph` library that implements a type-safe, conditional workflow for IP address analysis. The project fetches a public IP address, determines if it's IPv4 or IPv6, and splits it into component parts using a graph-based execution model. This example is useful for understanding conditional node execution, demonstrating type-safe state management, and showcasing async HTTP integration in graph workflows.

## Key Technologies

- **[pydantic-graph](https://ai.pydantic.dev/graph/)** - Core graph execution framework with type-safe node workflows
- **[Pydantic](https://docs.pydantic.dev/)** - Data validation and serialization for state and dependency models
- **httpx** - Async HTTP client for external API requests
- **Python 3.13+** - Modern Python with type hints and async support

