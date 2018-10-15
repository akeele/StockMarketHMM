from hmmlearn import hmm
import pickle

class RegimeHmmModel(object):
    """
    Hidden Markov Model for stock market regime detection
    """

    def __init__(self, daily_returns, n_states, n_iters, pickle_path):
        """
        Takes daily return series, number of hidden states in the model, number of max iterations and path for pickled model to be saved.
        Trains Gaussian HMM model with given parameters and pickles the trained model
        """
        self.daily_returns = daily_returns
        self.n_states = n_states
        self.n_iters = n_iters
        self.pickle_path = pickle_path
        # Train HMM
        self.trained_model = self._train(daily_returns, n_states, n_iters)
        self._dump_model(pickle_path)


    def _train(self, daily_returns, n_states, n_iters):
        """
        Train Gaussian hmm with given stock data
        """
        hmm_model = hmm.GaussianHMM(n_components=n_states, covariance_type="diag", n_iter=n_iters)
        trained_model = hmm_model.fit(self.daily_returns)
        return trained_model


    def _dump_model(self, pickle_path):
        """
        Pickle HMM model
        """
        pickle.dump(self.trained_model, open(pickle_path, "wb"))
