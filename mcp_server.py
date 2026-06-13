from fastmcp import FastMCP

mcp = FastMCP("fmcp_udhfg8cHvMjuO3VdpBCXfkozwEHwvp_icQUR0rg54wg")

@mcp.tool()
def saludar(nombre: str) -> str:
    """Saluda a una persona por su nombre."""
    return f"Hola, {nombre}! Este mensaje viene del MCP server."

@mcp.tool()
def sumar(a: int, b: int) -> int:
    """Suma dos números."""
    return a + b

if __name__ == "__main__":
    mcp.run()
