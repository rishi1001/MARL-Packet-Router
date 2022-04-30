from src.DDQN.Agent import DDQNAgent
from src.DDQN.ReplayMemory import ReplayMemory
import tqdm


class DDQNTrainerParams:
    def __init__(self):
        self.batch_size = 128
        self.num_steps = 1e6
        self.rm_pre_fill_ratio = 0.5
        self.rm_pre_fill_random = True
        self.eval_period = 5
        self.rm_size = 50000
        self.load_model = ""


class DDQNTrainer:
    def __init__(self, params: DDQNTrainerParams, agent: DDQNAgent):
        self.params = params
        self.replay_memory = ReplayMemory(size=params.rm_size)
        self.agent = agent
        # self.use_scalar_input = self.agent.params.use_scalar_input

        if self.params.load_model != "":
            print("Loading model", self.params.load_model, "for agent")
            self.agent.load_weights(self.params.load_model)

        self.prefill_bar = None

    def add_experience(self, state, action, reward, next_state):
        self.replay_memory.store((state, action, reward, next_state))
    

    def train_agent(self):
        if self.params.batch_size > self.replay_memory.get_size():
            return
        mini_batch = self.replay_memory.sample(self.params.batch_size)

        self.agent.train(mini_batch)


    # whaaat

    def should_fill_replay_memory(self):
        target_size = self.replay_memory.get_max_size() * self.params.rm_pre_fill_ratio
        if self.replay_memory.get_size() >= target_size or self.replay_memory.full:
            if self.prefill_bar:
                self.prefill_bar.close()
            return False

        if self.prefill_bar is None:
            print("Filling replay memory")
            self.prefill_bar = tqdm.tqdm(total=target_size)

        self.prefill_bar.update(self.replay_memory.get_size() - self.prefill_bar.n)

        return True