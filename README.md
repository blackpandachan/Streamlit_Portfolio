# Modern Portfolio Website with AI Chatbot

A sleek, modern portfolio website for Kelby James Enevold built with Streamlit and featuring a Claude-powered AI chatbot assistant. The chatbot allows prospective employers to ask questions about Kelby's experience, skills, and qualifications.

**NOTE:** *I still need to add new resume data and clean up a lot of the text being used for these containers and cards. Right now a lot of the markdown is very specific, and will eventually be fed via uploaded data instead of hard coded.*

## Features

- **Interactive Resume:** Modern, responsive design showcasing work experience, skills, and certifications
- **Interactive Skills Filtering:** Category-based skills visualization with radar charts and progress bars
- **Professional Testimonials:** Showcase recommendations from managers, clients, and colleagues
- **AI Chatbot:** Claude-powered assistant that can answer questions about qualifications and experience
- **Visual Timeline:** Career progression visualization with interactive components
- **Mobile-Friendly:** Responsive design that works on all devices
- **Dark Mode UI:** Professional dark-themed interface optimized for readability
- **Expandable Sections:** Detailed work experience and achievements in expandable sections
- **Quick Question UI:** Convenient buttons for common chatbot queries
- **Conversation Export:** Save your chat interactions for future reference

## Project Structure

```
portfolio_app/
├── app.py                # Main application entry point
├── requirements.txt      # Python dependencies
├── .env.example          # Example environment variables file
├── README.md             # Project documentation
├── DEPLOYMENT.md         # General deployment guide
├── GCP_DEPLOYMENT.md     # Google Cloud Platform deployment guide
├── docker-compose.yml    # Docker Compose configuration
├── Dockerfile            # Docker configuration
├── components/           # UI components
│   ├── __init__.py
│   ├── header.py         # Navigation and page header
│   ├── resume.py         # Resume display component with filtering
│   ├── timeline.py       # Interactive timeline component
│   └── chatbot.py        # Enhanced Claude-powered chatbot interface
├── data/                 # Data files
│   ├── __init__.py
│   └── resume_data.py    # Resume content structured as Python objects
├── styles/               # CSS and styling
│   └── main.css          # Custom CSS styles
└── utils/                # Utility functions
    ├── __init__.py
    └── claude_api.py     # Claude API integration
```

## Getting Started

### Prerequisites

- Python 3.9+ installed
- An Anthropic API key for Claude (optional - the app will work with mock responses without it)

### Installation

1. Clone this repository
   ```bash
   git clone https://github.com/yourusername/portfolio-website.git
   cd portfolio-website
   ```

2. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your environment variables (optional for Claude integration)
   ```bash
   cp .env.example .env
   ```
   Then edit the `.env` file to add your Anthropic API key.

### Running the Application

Use either the modular version:
```bash
streamlit run app.py
```

Or the standalone version:
```bash
streamlit run standalone_portfolio.py
```

The application will be available at http://localhost:8501

## Usage

### Customizing the Resume Data

To update the resume information, edit the files in the `data` directory:

- `resume_data.py`: Contains all the structured resume data including:
  - Personal information
  - Skills categorized by type with proficiency levels
  - Work experience with details and accomplishments
  - Certifications with issuing organizations and dates
  - Testimonials from managers, clients, and colleagues
  - Context information for the chatbot (including project highlights and FAQs)

### Customizing the Look and Feel

- Styling: Edit the CSS in the `styles/main.css` file
- Layout: Modify the components in the `components` directory
- Colors and themes: Update the color schemes in the CSS and inline styles

### Customizing the Chatbot

The enhanced chatbot can be configured by:

1. Editing the system prompt in the chatbot component
2. Providing an Anthropic API key via the UI or environment variables
3. Updating the quick question buttons in the chatbot component
4. Adding more FAQ entries to the chatbot context
5. Adding project highlights to the chatbot context for domain-specific responses

### Deployment

See the deployment guides for detailed instructions:

- [DEPLOYMENT.md](deployment_guides/DEPLOYMENT.md) - General deployment options:
  - Streamlit Cloud
  - Heroku
  - AWS Elastic Beanstalk
  - Docker
  - Docker Compose

- [GCP_DEPLOYMENT.md](deployment_guides/GCP_DEPLOYMENT.md) - Google Cloud Platform deployment:
  - Cloud Run with custom domain
  - Google Kubernetes Engine
  - CI/CD with GitHub Actions
  - DNS configuration for your domain

## How It Works

### Resume Display

The enhanced resume component visualizes your professional information using:

- Interactive category-based skills filtering with radar charts
- Visual timeline of career progression with expandable details
- Skills organized by category with proficiency indicators
- Styled certification cards with hover effects
- Professional testimonials section with quotes and attribution
- Downloadable resume option

### Enhanced Claude AI Chatbot

The improved chatbot allows employers to ask questions about your experience and qualifications:

1. Uses the Anthropic Claude API for natural, conversational responses
2. Provides quick question buttons for common queries
3. Features typing indicators for better user experience
4. Includes conversation export functionality
5. Leverages expanded context data for more accurate, specific responses:
   - Project highlights with metrics and technologies
   - Frequently asked questions with detailed answers
   - Comprehensive personal and professional background information

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- [Streamlit](https://streamlit.io/) for the web application framework
- [Anthropic](https://www.anthropic.com/) for the Claude AI assistant API
- [streamlit-chat](https://github.com/AI-Yash/st-chat) for the chat interface components
- [Matplotlib](https://matplotlib.org/) for data visualization
- [streamlit-extras](https://github.com/arnaudmiribel/streamlit-extras) for enhanced components
