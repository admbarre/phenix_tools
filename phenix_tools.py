from phenix_experiment import PhenixExperiment

def load_experiment(exp_dir):
    exp = PhenixExperiment(exp_dir)
    return exp
def get_description(exp):
    return exp.describe_exp()

if __name__ == "__main__":
    test_dir = "/Volumes/the_box/phenix/04-05 crawling__2023-04-05T11_32_49-Measurement 1"
    exp = load_experiment(test_dir)
    print(get_description(exp))
