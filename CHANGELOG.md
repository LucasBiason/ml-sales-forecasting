# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2025-10-29

### Added
- Complete ML pipeline with 4 Jupyter notebooks
- Random Forest model with 99,831 training samples
- FastAPI backend with MVC architecture
- React frontend with TypeScript and TailwindCSS
- Docker multi-stage builds for API and Frontend
- 75+ unit tests with 90%+ coverage
- GitHub Actions CI/CD pipeline
- Postman collection with embedded documentation
- Architecture diagrams and complete documentation

### Features

#### Machine Learning
- Exploratory data analysis on UK Property Sales dataset
- Feature engineering (postcode_region extraction)
- Model selection (Random Forest chosen)
- Hyperparameter tuning with RandomizedSearchCV
- Final pipeline with cross-validation
- Model artifacts export (.joblib files)

#### Backend API
- Health check endpoints (/ and /health)
- Model info endpoint (/api/v1/model/info)
- Prediction endpoint (/api/v1/predict)
- Pydantic validation for all inputs
- Error handling with proper HTTP status codes
- CORS configuration
- Multi-worker support (4 workers in production)

#### Frontend
- Modern UI with TailwindCSS
- Responsive design (desktop + mobile)
- Dark mode support
- Real-time API status indicator
- Form validation
- Loading states
- Error handling with user-friendly messages
- Price formatting in GBP
- Confidence interval display

#### DevOps
- Docker Compose with profiles (test, api, frontend, full)
- Multi-stage Dockerfiles (optimized builds)
- Entrypoint CLI pattern
- Makefile automation
- Hot reload in development
- GitHub Actions workflow
- Coverage reports (HTML + terminal)

### Technical Details

#### Models
- Random Forest: 100 estimators
- Features: 6 (encoded)
- R² Score: 11.16% (general), 27% (properties under £1M)
- MAE: £86,796
- Cross-validation R²: 0.4390 (log scale)

#### Stack
- Python 3.13
- FastAPI 0.104+
- React 18
- TypeScript
- TailwindCSS 3.4
- scikit-learn 1.3+
- pytest 7.4+
- Docker & Docker Compose
- Nginx (Alpine)
- Node 20 (Alpine)

### Documentation
- README.md with quick start and examples
- ARCHITECTURE.md with detailed technical docs
- Postman collection with 10 saved responses
- Architecture diagrams (Mermaid source included)
- Screenshots of running application
- Code 100% PEP8/Flake8 compliant
