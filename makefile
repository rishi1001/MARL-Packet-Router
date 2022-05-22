
run: 
	python3 main.py $(folder)

run_hpc:
	qsub pbsbatch.sh

watch:
	watch qstat -u $USER



setup:
	@echo "Setting up..."
	@pip install torch torchvision torchaudio
	@pip install numpy
	@pip install tqdm
	@pip install matplotlib

copy:
	@echo "Copying files..."
	@read -p "Enter User Name:" user;\
	name=$$user@hpc.iitd.ac.in; \
	scp -r ./Maps $$name:./marl \
	scp -r ./src $$name:./marl  \
	scp -r ./model_parameters $$name:.marl  \
	scp -r ./Plots $$name:.marl   \
	scp config.ini main.py makefile pbsbatch.sh $$name:.marl


clean:
	@echo "Cleaning up..."
	rm -r Plots


