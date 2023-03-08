import bnlearn as bn


def printModel(model):
	bn.plot(model, verbose=0)
	bn.print_CPD(model)


def main():
	model = bn.import_DAG('cancer.bif')
	df = bn.sampling(model, n=1000000, verbose=0)
	model_new = bn.structure_learning.fit(df, verbose=0, methodtype='cs')
	model_new_w_params = bn.parameter_learning.fit(model_new, df, verbose=0)
	model_w_params = bn.parameter_learning.fit(model, df, verbose=0)

	printModel(model)
	printModel(model_w_params)
	printModel(model_new)
	printModel(model_new_w_params)


if __name__ == '__main__':
	main()
