# Haidut Collected Works

<div align="center">
  <img src="https://github.com/user-attachments/assets/ea470d86-cd36-4a90-949c-fc74bc899061" width="270" height="420" alt="Book Cover">
  
  <br>
  <br>

  [![Follow @ibuybooks](https://img.shields.io/badge/Follow%20%40ibuybooks-000000?logo=X&logoColor=white&style=for-the-badge)](https://x.com/ibuybooks)
  [![LaTeX](https://img.shields.io/badge/LaTeX-008080?style=for-the-badge&logo=latex&logoColor=white)](#)
  [![License](https://img.shields.io/badge/Free%20for%20Non--Commercial%20Use-007bff?style=for-the-badge&logo=github&logoColor=white&labelColor=282828&color=007bff)](#)
  ![Made with ❤️ by Gavin](https://img.shields.io/badge/Made_with_❤️_by-Gavin-red?style=for-the-badge)
      
  [![Stars](https://img.shields.io/github/stars/ibuybooks/haidut-collected-works?style=for-the-badge&color=2F323A)](https://github.com/ibuybooks/haidut-collected-works/stargazers)
  [![Size](https://img.shields.io/github/repo-size/ibuybooks/haidut-collected-works?style=for-the-badge&color=2F323A)](https://github.com/ibuybooks/haidut-collected-works)
  [![Downloads](https://img.shields.io/github/downloads/ibuybooks/haidut-collected-works/total?style=for-the-badge&color=2F323A)](https://github.com/ibuybooks/haidut-collected-works/releases)

  <br>

  >*"Our intelligence develops as we grow into the world, such as it is, and our world includes things that we learn about, and the people that we learn from."*
  >
  > — Ray Peat
</div>

<br>

>[!NOTE]
> **MEDICAL ADVICE DISCLAIMER**
> 
> The information contained in this repository is for educational and informational purposes only and is not intended as medical advice. You should not rely on this information to make decisions about your health or medical treatment. The author is not responsible for any use or misuse of this content.

<br>

<div align="center">
  <h2>⚡ Quick Start</h2>
  <h3>Download the Latest Release</h3>
  <p>Download the Latest PDFs</p>
  
  [![Download][Download-Badge]][Download-Link]

  [Download-Badge]: https://img.shields.io/badge/Download_Latest_Release-2563eb?style=for-the-badge&logo=github&logoColor=white&labelColor=1e40af
  [Download-Link]: https://github.com/ibuybooks/haidut-collected-works/releases/latest/
  
  <sup>📖 View the README for more information.</sup>
</div>

<div align="center">
  <h2>📌 README</h2>
</div>

>[!CAUTION]
> **CONTENT ACCURACY NOTICE**
> 
> This repository contains content that has been automatically parsed from scraped web data. While care has been taken to manually verify the accuracy and quality of the data, verification of all content is not possible. Please exercise caution when using or referencing anything contained within this content.
<h3>📎 About:</h3>

**Haidut Collected Works**  
*A Comprehensive Collection of Haidut's Forum Posts, Replies, and Articles.*

This project is a high-quality LuaLaTeX compilation of Haidut's work, posted on the Ray Peat Forum from 2013 to 2024. Each article presented includes the main content, as well as the replies to which Haidut responded, any included or cited figures, and the references. The articles are compiled on a yearly basis, and there are twelve volumes in total.

<h3>📏 Improvements:</h3>

- Removed duplicate replies, quotes, and text.
- Anonymized usernames.
- URLs and references are converted into a proper citations.
- Implimented proper scientific notation (e.x., CO2 -> CO<sub>2</sub>).
- Standarized capitalizations (e.x., "dna" -> "DNA").
- Corrected spelling, grammar, and capitalizations.
- Implimented proper fancy quotes (using csquotes).
- Removed formatting (bold, italics, underline, color).
- Removed irrelevant replies ("Thanks," etc.)
- And more!

<h3>🔖 Notes:</h3>

- Standard 8.5"x11" paper size.
- 12 volumes, 2013-2024.

<h3>🔧 Workflow:</h3>

```mermaid
%%{init: {
     "theme": "base",
     "themeVariables": {
       "primaryColor": "#f8fafc",
       "primaryTextColor": "#1e293b",
       "primaryBorderColor": "#64748b",
       "lineColor": "#64748b",
       "secondaryColor": "#e2e8f0",
       "tertiaryColor": "#f1f5f9",
       "background": "#ffffff",
       "mainBkg": "#f8fafc",
       "secondBkg": "#e2e8f0",
       "tertiaryBkg": "#f1f5f9",
       "fontSize": "10px",
       "fontFamily": "Inter, system-ui, sans-serif"
     },
     "flowchart": { 
       "nodeSpacing": 10, 
       "rankSpacing": 20,
       "curve": "linear"
     }
}}%%
flowchart TD
    subgraph Startup
        A1["Load CoEdIT"]
        A2["Load SciBERT<br>+ Tokenizer"]
    end
    Startup -->|File| FILES["Add File"]
    Startup -->|Directory| WALK["Walk Directory"]
    WALK --> FILES
    FILES --> PROC{{Next File}}
    PROC --> PARSE["Parse HTML"]
    PARSE --> META["Extract Metadata"]
    PARSE --> USER["Build Username Map<br>+ Anonymize"]
    PARSE --> POSTS["Iterate Posts"]
    POSTS -->|First Haidut Post| ART["Main Article"]
    POSTS -->|Other Posts| DISC["Replies / Comments"]
    ART --> PIPE["CoEdIT + SciBERT"]
    DISC --> PIPE
    PIPE --> LATEX["Assemble LaTeX"]
    LATEX --> WRITE["Write .tex"]
    LATEX --> BIB["Update Bibliography"]
    WRITE --> NEXT{More Files?}
    NEXT -->|Yes| PROC
    NEXT -->|No| DONE["All Files Done"]
    DONE --> REVIEW["Manual Review & Edits"]
    REVIEW --> PUBLISH(("Publish"))
    
    %% Clean minimal styling
    classDef process fill:#f1f5f9,stroke:#64748b,stroke-width:1px,color:#1e293b;
    classDef decision fill:#fef3c7,stroke:#d97706,stroke-width:1px,color:#92400e;
    classDef terminal fill:#dcfce7,stroke:#16a34a,stroke-width:1px,color:#166534;
    classDef data fill:#dbeafe,stroke:#2563eb,stroke-width:1px,color:#1d4ed8;
    
    class A1,A2,A3,FILES,PARSE,META,USER,POSTS,ART,DISC,PIPE,LATEX,WRITE,BIB,REVIEW process;
    class CLI,WALK,DONE data;
    class PATHS,PROC,NEXT decision;
    class PUBLISH terminal;
```

<h3>🧮 Project Structure:</h3>

```
.
├── Scripts/                      # Utility Scripts
│   └── Remove_Blank_Pages.py     # Extra Blank Page Removal Utility
│
├── Common/                       # Shared Resources
│   ├── Fonts/                    # Fonts
│   │   ├── Open_Sans/            # Open Sans Font Family
│   │   │   └── *.ttf             # Regular, Bold, Italic, Light, Medium, etc.
│   │   └── EB_Garamond/          # EB Garamond Font Family
│   │       └── *.ttf             # Regular, Bold, Italic, Medium, etc.
│   ├── Tufte-Book.cls            # Tufte-Style Book Class
│   └── Tufte-Common.def          # Class Definitions
│
└── Years/                        # Posts Sorted by Year
    └── [YEAR]/                   # Year Folder
        ├── Articles/             # Articles
        │   └── Articles.zip      # Article TeX Files (Compressed for GitHub)
        ├── Images/               # Images
        │   └── [TITLE].[NUM].jpg # Image Named After Article
        ├── Cover.tex             # Cover
        ├── [YEAR].tex            # Main TeX File
        └── Bibliography.bib      # Bibliography
```

<div align="center">
  <h2>⚒️ Building from Source</h2>
</div>

<h3>📄 Instructions:</h3>

```bash
# Clone the repository:
git clone https://github.com/ibuybooks/haidut-collected-works.git

# Un-zip the articles:
unzip Years/[YEAR]/Articles/Articles.zip -d Years/[YEAR]/Articles/

# Install required packages:
tlmgr install babel babel-english csquotes microtype fontspec xparse lua-ul graphicx adjustbox xurl extdash hyperref fancyhdr changepage makeidx titlesec tcolorbox chemfig luacode tikz chngcntr etoolbox truncate biblatex biber tufte-latex collection-fontsrecommended collection-latexrecommended

# Compile the document:
lualatex [YEAR].tex

# Process the bibliography
biber [YEAR]

# Compile the document with the bibliograpy:
lualatex [YEAR]
lualatex [YEAR]

# (Optional) remove extra blank pages (recommended):
# Install required packages:
pip3 install pymupdf

# Remove blank pages:
python3 Scripts/Remove_Blank_Pages.py Years/[YEAR]/[YEAR].pdf
```
