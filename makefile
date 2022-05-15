run: 
	python3 main.py

setup:
	@echo "Setting up..."
	@pip install torch torchvision torchaudio
	@pip install numpy
	@pip install tqdm
	@pip install matplotlib

clean:
 	@echo "Cleaning up..."
	rm -r Plots
