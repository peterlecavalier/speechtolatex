# Speech-To-LaTeX

Our platform creates a seamless experience for technical authors to effectively write mathematical papers in LaTeX format - without needing to learn how to code.

Simply record audio and our tool will translate it into LaTeX document, with integrated PDF compilation.

[Client-Side GitHub](https://github.com/moreSalt/speechtolatex-client)

## Directories
- **Database Code** - Generation of initial MySQL databases
- **Latex-PDF-Compile** - Compilation of LaTeX docs into PDFs
- **api** - Python API for handling full-stack integration
- **modelInfo** - Files related to the model
- **scrape_latex** - Scraping LaTeX files for training and testing
- **speech-to-text-api** - API code for speech-to-text model
- **text-to-tex-api** - API code for text-to-TeX model

## Technologies
- **SvelteKit** (Frontend)
- **Vercel** (Hosting and deployment)
- **HuggingFace** (Speech-to-text ML model)
- **OpenAI API** (Text-to-TeX ML model)
- **Google Cloud Platform** (Model hosting + cloud infrastructure)
- **MySQL** (User and file storage)
- **ProxySQL** (Database load balancing)
- **Python + Flask** (API for full-stack)
- **Google Cloud Storage** (LaTeX Training Docs)

## Contributors
- Logan Barnhart
- Oscar Carlek
- Claudia Chen
- Tobias Jacobson
- Peter LeCavalier
- Paul Rodriguez
