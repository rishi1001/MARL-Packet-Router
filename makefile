run_hpc:
	qsub pbsbatch.sh

watch:
	watch qstat -u $USER


run: 
	python3 main.py

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
	scp -r ./Maps $$name:./MARL-Packet-Router/ \
	scp -r ./src $$name:./MARL-Packet-Router/  \
	scp -r ./model_parameters $$name:./MARL-Packet-Router/  \
	scp -r ./Plots $$name:./MARL-Packet-Router/   \
	scp config.ini main.py makefile pbsbatch.sh $$name:./MARL-Packet-Router/


clean:
	@echo "Cleaning up..."
	rm -r Plots


