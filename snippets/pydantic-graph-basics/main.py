import asyncio
import ipaddress
from typing import Optional, Union
import httpx
from pydantic import BaseModel
from pydantic_graph import BaseNode, Graph, End, GraphRunContext


class State(BaseModel):
    """Shared state that flows between nodes in the graph."""

    proxy_url: Optional[str] = None
    current_ip: Optional[str] = None
    ip_type: Optional[str] = None  # 'ipv4' or 'ipv6'


class Dependencies(BaseModel):
    """External dependencies available to all nodes."""

    model_config = {"arbitrary_types_allowed": True}

    http_client: httpx.AsyncClient


class FetchIPNode(BaseNode[State, Dependencies, list[str]]):
    """Node that fetches the current public IP address."""

    async def run(
        self, ctx: GraphRunContext[State, Dependencies]
    ) -> Union["EvaluateIPTypeNode", End[list[str]]]:
        print("Fetching current IP address...")

        # Use a service to get current public IP
        # Note: If a proxy_url is provided in state, it could be used here
        # For demonstration, we'll show how to access it
        if ctx.state.proxy_url:
            print(f"Proxy URL available: {ctx.state.proxy_url}")

        try:
            response = await ctx.deps.http_client.get("https://httpbin.org/ip")
            response.raise_for_status()
            ip_data = response.json()
            current_ip = ip_data.get("origin", "").split(",")[0].strip()

            print(f"Current IP: {current_ip}")

            # Update state and continue to evaluation node
            ctx.state.current_ip = current_ip
            return EvaluateIPTypeNode()
        except Exception as e:
            print(f"Error fetching IP: {e}")
            ctx.state.current_ip = "error"
            return End([])


class EvaluateIPTypeNode(BaseNode[State, Dependencies, list[str]]):
    """Node that determines if the IP is IPv4 or IPv6."""

    async def run(
        self, ctx: GraphRunContext[State, Dependencies]
    ) -> Union["ProcessIPv4Node", "ProcessIPv6Node", End[list[str]]]:
        if not ctx.state.current_ip or ctx.state.current_ip == "error":
            print("No valid IP to evaluate")
            return End([])

        try:
            ip_obj = ipaddress.ip_address(ctx.state.current_ip)
            if isinstance(ip_obj, ipaddress.IPv4Address):
                ip_type = "ipv4"
                print(f"Detected IPv4 address: {ctx.state.current_ip}")
                ctx.state.ip_type = ip_type
                return ProcessIPv4Node()
            elif isinstance(ip_obj, ipaddress.IPv6Address):
                ip_type = "ipv6"
                print(f"Detected IPv6 address: {ctx.state.current_ip}")
                ctx.state.ip_type = ip_type
                return ProcessIPv6Node()
            else:
                print(f"Unknown IP type: {ctx.state.current_ip}")
                return End([])
        except ValueError as e:
            print(f"Invalid IP address format: {ctx.state.current_ip}, error: {e}")
            return End([])


class ProcessIPv4Node(BaseNode[State, Dependencies, list[str]]):
    """Node that processes IPv4 addresses by splitting on periods."""

    async def run(self, ctx: GraphRunContext[State, Dependencies]) -> End[list[str]]:
        if not ctx.state.current_ip:
            return End([])

        ip_parts = ctx.state.current_ip.split(".")
        print(f"IPv4 parts: {ip_parts}")

        return End(ip_parts)


class ProcessIPv6Node(BaseNode[State, Dependencies, list[str]]):
    """Node that processes IPv6 addresses by splitting on colons."""

    async def run(self, ctx: GraphRunContext[State, Dependencies]) -> End[list[str]]:
        if not ctx.state.current_ip:
            return End([])

        ip_parts = ctx.state.current_ip.split(":")
        print(f"IPv6 parts: {ip_parts}")

        return End(ip_parts)


async def main():
    """Main function that creates and runs the IP analysis graph."""
    print("Pydantic Graph IP Analysis Demo")
    print("=" * 40)

    # Create the graph with all nodes
    graph = Graph(
        nodes=[FetchIPNode, EvaluateIPTypeNode, ProcessIPv4Node, ProcessIPv6Node],
        name="IP Analysis Graph",
    )

    # Set up initial state and dependencies
    initial_state = State(
        proxy_url="http://squid.corp.redhat.com:3128"
    )  # Example proxy URL

    async with httpx.AsyncClient() as client:
        dependencies = Dependencies(http_client=client)

        # Run the graph starting from FetchIPNode
        result = await graph.run(
            state=initial_state, deps=dependencies, start_node=FetchIPNode()
        )

        print("\n" + "=" * 40)
        print("Graph execution completed!")
        print(f"Final state: {result.state}")
        print(f"IP Parts: {result.output}")

        if result.output:
            print(f"Successfully parsed IP into {len(result.output)} parts")
        else:
            print("No IP parts generated (likely due to error)")


if __name__ == "__main__":
    asyncio.run(main())
