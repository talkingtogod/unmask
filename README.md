
# UNMASK - GitHub Email Extractor

A powerful Python tool for extracting email addresses from GitHub repositories and public events. UNMASK provides comprehensive GitHub user analysis with beautiful terminal interface and detailed reporting capabilities.

## Description

UNMASK is an advanced GitHub reconnaissance tool that scans public repositories, commits, and events to discover email addresses associated with a target user. The tool features an intuitive interface with real-time progress tracking and detailed user profiling.

## Features

- **Comprehensive Email Discovery**: Extracts emails from repository commits and public events
- **User Profile Analysis**: Displays detailed GitHub user information
- **Advanced Filtering Options**: Include/exclude hidden emails and apply user-specific filters
- **Beautiful Interface**: Colorful terminal interface with progress bars and animations
- **Multiple Scan Modes**: Quick scan for fast results or advanced scan with customizable options
- **Export Functionality**: Save results to formatted text files
- **Rate Limit Handling**: Built-in GitHub API rate limit management
- **Cross-Platform Support**: Compatible with Windows, Linux, and macOS

## Installation

### Prerequisites

- Python 3.6 or higher
- pip package manager
- Internet connection

#

### Manual Installation

Install required packages manually:
```bash
pip install requests==2.28.1
pip install prompt_toolkit==3.0.36
pip install pystyle==2.9
```

## Usage

### Basic Usage

1. Run the script:
```bash
python unmask.py
```

2. Enter the target GitHub username when prompted

3. Choose scan type:
   - **Quick Scan**: Uses default settings for faster results
   - **Advanced Scan**: Provides customizable options

### Advanced Configuration

When using Advanced Scan mode, you can configure:

- **Hidden Emails**: Include or exclude @users.noreply.github.com addresses
- **User Filter**: Filter results to show only emails from the target user's activity

### Example Output

```
===============================================
              USER INFORMATION
===============================================

Username        : johndoe
Name            : John Doe
Profile URL     : https://github.com/johndoe
Email           : john@example.com
Company         : Example Corp
Location        : San Francisco, CA
Account Type    : User
Followers       : 150
Following       : 75
Public Repos    : 25
User ID         : 12345678
Created         : 2020-01-15T10:30:00Z

===============================================
              EXTRACTED EMAILS
===============================================

Email #1: john.doe@company.com
Sources:
  1. Repo: https://github.com/johndoe/project1, User: johndoe
  2. Public Commit, User: johndoe

Email #2: j.doe@personal.com
Sources:
  1. Repo: https://github.com/johndoe/project2, User: johndoe
```

## Requirements

### System Requirements

- **Operating System**: Windows 10+, macOS 10.14+, or Linux
- **Python Version**: 3.6 or higher
- **Memory**: 256 MB RAM minimum
- **Storage**: 50 MB free space

### Python Dependencies

- **requests**: HTTP library for API calls
- **prompt_toolkit**: Enhanced input prompts with auto-completion
- **pystyle**: Terminal styling and colors

## Configuration

### API Rate Limits

The tool respects GitHub's API rate limits:
- **Unauthenticated requests**: 60 requests per hour
- **Authenticated requests**: 5,000 requests per hour (if using personal access token)

To increase rate limits, add your GitHub token to the headers in the script:
```python
self.headers = {
    "User-Agent": get_random_user_agent(),
    "Authorization": "token YOUR_GITHUB_TOKEN"
}
```

### Scan Options

#### Quick Scan
- Includes hidden emails (@users.noreply.github.com)
- No user-specific filtering
- Faster execution time

#### Advanced Scan
- Customizable hidden email inclusion
- Optional user-specific filtering
- More detailed analysis

## Output Formats

### Terminal Output
- Real-time progress tracking
- Colorized results with source attribution
- Summary statistics

### File Export
- Plain text format with structured layout
- Includes user information and scan summary
- Easy to parse and analyze

## Error Handling

The tool handles various error conditions:

- **User Not Found**: Clear error message for non-existent users
- **Rate Limit Exceeded**: Automatic detection with retry suggestions
- **Network Issues**: Graceful handling of connection problems
- **Invalid Input**: User-friendly error messages with correction prompts

## Legal Disclaimer

**IMPORTANT**: This tool is for educational and authorized security research purposes only.

### Ethical Usage Guidelines

1. **Authorization Required**: Only use on accounts you own or have explicit permission to test
2. **Respect Privacy**: Do not use for unauthorized surveillance or harassment
3. **Follow Laws**: Comply with all applicable local, state, and federal laws
4. **Responsible Disclosure**: Report vulnerabilities through proper channels
5. **Rate Limits**: Respect GitHub's terms of service and API limitations

### Prohibited Uses

- Unauthorized access to private information
- Harassment or stalking of individuals
- Commercial exploitation without consent
- Violation of GitHub's terms of service
- Any illegal activities

The developers are not responsible for misuse of this tool.

## Troubleshooting

### Common Issues

#### Import Errors
```
ModuleNotFoundError: No module named 'pystyle'
```
**Solution**: Install missing dependencies with pip install

#### Rate Limit Errors
```
GitHub API rate limit reached
```
**Solution**: Wait for rate limit reset or use GitHub token

#### Display Issues on Windows
```
Colors not displaying correctly
```
**Solution**: Enable ANSI color support in Windows Terminal

#### Permission Errors
```
Permission denied when saving files
```
**Solution**: Run with appropriate permissions or change output directory

### Performance Tips

1. **Use Quick Scan** for basic email discovery
2. **Enable user filtering** to reduce noise in results
3. **Use GitHub token** to increase API rate limits
4. **Run during off-peak hours** to avoid rate limiting

## Contributing

We welcome contributions to improve UNMASK!

### How to Contribute

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

### Development Setup

```bash
git clone https://github.com/yourusername/unmask.git
cd unmask
pip install -r requirements-dev.txt
```

### Code Style

- Follow PEP 8 guidelines
- Use meaningful variable names
- Add comments for complex logic
- Include docstrings for functions

### Reporting Issues

When reporting bugs, please include:
- Python version
- Operating system
- Error messages
- Steps to reproduce

## Changelog

### Version 2.0.0
- Added pystyle interface with beautiful colors
- Implemented progress bars and loading animations
- Enhanced user profile display
- Added advanced scan configuration
- Improved error handling

### Version 1.5.0
- Added file export functionality
- Implemented user filtering options
- Enhanced GitHub API error handling
- Added comprehensive user information display

### Version 1.0.0
- Initial release
- Basic email extraction functionality
- Simple terminal interface

## License

This project is licensed under the MIT License.

```
MIT License

Copyright (c) 2024 UNMASK Developers

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Acknowledgments

- GitHub API for providing comprehensive user and repository data
- The Python community for excellent libraries and tools
- Security researchers who inspire responsible disclosure practices
- Contributors who help improve and maintain this project

## Contact

For questions, suggestions, or security reports:
- GitHub Issues: Open an issue in the repository
- Discord: @midlegg

- No emojis as requested

The file will be created in the same directory as your script and contains all the necessary information for a professional GitHub repository.
