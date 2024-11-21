# Invoicify

## Project Overview
This project provides a streamlined e-invoicing solution for small-to-medium enterprises (SMEs), enabling efficient invoice creation, validation, and sending, while ensuring compliance with A-NZ PEPPOL BIS 3.0 standards.

### Key Features
1. **Invoice Creation**
    - Supports PDF, JSON uploads, or manual input via a user-friendly GUI.
    - Uses OCR (UpBrains AI) to extract data from PDF invoices and convert it into UBL2.1 XML format.
2. **Invoice Validation**
    - Validates XML invoices using the ESS validator API for compliance.
    - Generates detailed error reports for failed validations.
3. **Invoice Sending**
    - Allows sending validated invoices via email.
    - Supports bulk operations for increased efficiency.
4. **Invoice Management**
    - Enables authenticated users to edit, delete, and manage their invoices.
5. **User-Centric Design**
    - Material-UI-based interface for a consistent and familiar user experience.
    - Responsive design supporting desktop and mobile use.

### Installation
The application is dockerised for easy deployment:
1. Clone the repository.
2. Create a `.env` file in `backend/` with required variables
3. Run `docker-compose up`.
4. Access the app at `localhost:3000`.

Note: Python version 3.9+ is required.


### Technical Design
- **Architecture**: Modular design comprising authentication, invoice processing, and database services.
- **Backend**: Python (FastAPI) with SQLAlchemy for database management.
- **Frontend**: React.js using Material-UI for UI consistency.

### Limitations & Future Improvements
- Improve OCR data accuracy for PDF invoice validation.
- Expand file format support (e.g., CSV, TXT).
- Integrate with popular accounting tools like Xero and QuickBooks.