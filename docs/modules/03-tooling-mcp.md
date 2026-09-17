# Module 3 lab: Tooling, MCP, and execution environments

## Goal

Practice a narrow tool boundary that accepts a read request and denies an unapproved write.

## Steps

1. Read `examples/mcp_request.json` and `scripts/mcp/tool_boundary.py`.
2. Run the approved request:

   ```bash
   python3 scripts/mcp/tool_boundary.py \
     --request examples/mcp_request.json \
     --output /tmp/mcp-response.json
   cat /tmp/mcp-response.json
   ```

3. Create a copy of the request with `"operation": "write_file"` and run it. The process should exit nonzero and write a denied decision.
4. Identify the boundary checks: tool allowlist, operation allowlist, path restriction, and audit record.
5. Explain the difference between the MCP protocol shape and the authorization policy. A protocol can carry a request; it does not make the request safe.

## Codespaces and Actions

Use Codespaces for interactive inspection and Copilot CLI work. Use Actions for repeatable, permissioned automation. Keep writes behind explicit permissions and approval gates.

