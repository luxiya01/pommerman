'''An example to show how to set up an pommerman game programmatically'''
import pommerman
from pommerman import agents
from pytree_agent import PyTreeAgent


def main():
    '''Simple function to bootstrap a game.

       Use this as an example to set up your training env.
    '''
    # Print all possible environments in the Pommerman registry
    print(pommerman.REGISTRY)

    # Create a set of agents (exactly four)
    agent_list = [
        #agents.PlayerAgent(agent_control="arrows"),
        agents.SimpleAgent(),
        PyTreeAgent(),
        agents.SimpleAgent(),

        #        agents.RandomAgent(),
        PyTreeAgent()
        # agents.DockerAgent("pommerman/simple-agent", port=12345),
    ]
    # Make the "Free-For-All" environment using the agent list
    env = pommerman.make('PommeRadioCompetition-v2', agent_list)
    env.seed(400)

    # Run the episodes just like OpenAI Gym
    for i_episode in range(1):
        state = env.reset()
        done = False
        while not done:
            env.render()
            actions = env.act(state)
            state, reward, done, info = env.step(actions)
        print('Episode {} finished'.format(i_episode))
        print(reward)
    env.close()


if __name__ == '__main__':
    main()
