# THUAI7 Agent Template (Python)

Python agent template for the 7th Tsinghua University Artificial Intelligence Challenge.

## Environment

The agent template is developed under `python 3.9.16`.

## How to Use

### Run the Agent

1. Download latest release from [here](https://github.com/thuasta/thuai-7-agent-template-python/releases).
2. Check `src/` folder.
3. Run `pip install -r requirements.txt`.
4. Run `python main.py`.
  - Additional arguments:
    - --host: Choose a server to connect.
    - --port: Choose a port to connect.
    - --token: Choose a token for connection.
  - For example, if you input `python main.py --host 127.0.0.1 --port 8080 --token player1`, the agent will try to connect `127.0.0.1:8080` with token `"player1"`
  - Note that a running server is necessary for connection.

### Create Your Own Agent

Follow the instruction in `main.py` to create your own agent.

### Interfaces

Yo can see all interfaces in `agent_entry.py`.

## Contributing

Ask questions by creating an issue.

PRs accepted.

## License

GPL-3.0-only © Student Association of Science and Technology, Department of Automation, Tsinghua University
