# SLCM Bundles Distribution Automation

SLCM Bundles Distribution Automation is a Python-based automation tool designed to streamline the camp allocation process for SLCM (Student Life Cycle Management) bundles. It simplifies and accelerates the workflow by eliminating manual tasks and providing automated sorting capabilities.

## Features

- **Automated Data Collection**: Scrapes bundle details from the SLCM website and converts them into Excel files.
- **Data Processing**: Processes the scraped data and generates distributions based on specified configurations.
- **Camp Allocation**: Allocates bundles to different camps based on predefined rules and target values.
- **Output Generation**: Generates Excel files containing the final camp distributions for each QP (Question Paper) code.

## Getting Started

### Prerequisites

- Python 3.10
- Google Chrome (for web scraping)
- Required Python packages (listed in `requirements.txt`)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/slcm-bundles-distribution-automation.git
   ```

2. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

3. Download the appropriate `chromedriver` for your system and place it in the `configs` directory.

### Configuration

1. Open the `configs/configurations.yaml` file and update the following settings:

   - `distributionDetailsFile`: Path to the file containing distribution details.
   - `undallocatedBundlesFolder`: Path to the folder where scraped bundle details will be saved.
   - `generatedDistributionsSaveFolder`: Path to the folder where generated distributions will be saved.
   - `mergedOutputFolderPath`: Path to the folder where merged output files will be saved.
   - `campList`: List of camp names (e.g., `["Thiruvananthapuram", "Kollam", "Pathanamthitta", "Alappuzha"]`).
   - `qpSeries`: Series identifier for QP codes (e.g., `"P"`, `"Q"`, `"R"`).
   - `qpStartRange`: Starting range of QP codes.
   - `qpEndRange`: Ending range of QP codes.
   - `examName`: Name of the exam.
   - `nopecha`: Your NopeCHA API key (for captcha solving).
   - `username` and `password`: Credentials for the SLCM website.

2. Ensure that the `distributionDetailsFile` name follows the format `<examName>_distribution.xlsx`, where `<examName>` is the value specified for the `examName` configuration.

### Usage

1. Run the `bundle_details_collector.py` script to scrape bundle details from the SLCM website and generate Excel files:

   ```bash
   python bundle_details_collector.py
   ```

2. Run the `distributionMaker.py` script to generate camp distributions based on the scraped data:

   ```bash
   python distributionMaker.py
   ```

The generated distributions will be saved as Excel files in the `generatedDistributionsSaveFolder` specified in the configuration.

## Project Structure

```
slcm-bundles-distribution-automation/
├── configs/
│   ├── configurations.yaml
│   └── chromedriver
├── Inputs/
│   ├── Distribution/
│   └── Grabbed_Results/
├── Outputs/
│   ├── Generated_Distributions/
│   └── merged_outputs/
├── bundle_details_collector.py
├── distributionMaker.py
├── extract_distribution_xl.py
├── four_camp_distribution.py
├── labs/
├── requirements.txt
└── README.md
```

- `configs/`: Contains the configuration file (`configurations.yaml`) and the `chromedriver` executable.
- `Inputs/Distribution/`: Directory for storing distribution detail files.
- `Inputs/Grabbed_Results/`: Directory for storing scraped bundle detail files.
- `Outputs/Generated_Distributions/`: Directory for saving generated camp distribution files.
- `Outputs/merged_outputs/`: Directory for saving merged output files.
- `bundle_details_collector.py`: Script for scraping bundle details from the SLCM website.
- `distributionMaker.py`: Script for generating camp distributions based on the scraped data.
- `extract_distribution_xl.py`: Helper module for extracting data from distribution detail files.
- `four_camp_distribution.py`: Core module for camp allocation and distribution generation.
- `labs/`: Directory containing experimental code for future enhancements.
- `requirements.txt`: File listing the required Python packages.

## Contributing

Contributions to this project are welcome. If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
