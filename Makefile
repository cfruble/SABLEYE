# makefile to automate Bateman matrix creation

DOWNLOAD_URL = https://www.nndc.bnl.gov/endf-b8.0/zips/ENDF-B-VIII.0.zip
DOWNLOADED_FILE = ENDF-B-VIII.0.zip
EXTRACT_DIR = rawENDF_Data

.PHONY: all clean

all: $(EXTRACT_DIR)
	@echo "Dowloading Zip_Bomb.zip..."
	@echo "Dowloading $(DOWNLOADED_FILE)..."
	@test -f $(DOWNLOADED_FILE) || wget -O $(DOWNLOADED_FILE) $(DOWNLOAD_URL)

$(EXTRACT_DIR): $(DOWNLOADED_FILE)
	@echo "Unzipping $(DOWNLOADED_FILE) to $(EXTRACT_DIR)..."
	@mkdir -p $(EXTRACT_DIR)
	@unzip $(DOWNLOADED_FILE) -d $(EXTRACT_DIR)

clean:
	@echo "Cleaning up..."
	@rm -f $(DOWNLOADED_FILE)
	@rm -rf $(EXTRACT_DIR)