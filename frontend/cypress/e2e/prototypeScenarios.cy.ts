/// <reference types="cypress" />

const registerDetails = {
  'first-name': 'John',
  'last-name': 'Smith',
  email: 'smith@gmail.com',
  password: 'smith123',
};

describe('test user login', () => {
  beforeEach(() => {
    cy.visit('localhost:3000');

    cy.fixture('api_responses/authRegister').then((response) => {
      cy.intercept('POST', '/auth/register', (req) => {
        req.reply(response);
      });
    })

    cy.fixture('api_responses/authLogin').then((response) => {
      cy.intercept('POST', '/auth/login', (req) => {
        req.reply(response);
      });
    });

  });

  it('should navigate to the app home screen successfully', () => {
    cy.url().should('include', 'localhost:3000');
  });

  it('should navigate to the login screen successfully', () => {
    cy.get('[data-cy="login"]').click();
    cy.url().should('include', 'localhost:3000/sign-in');
  });

  it('should sign up successfully', () => {
    cy.get('[data-cy="login"]').click();
    cy.url().should('include', 'localhost:3000/sign-in');
    cy.get('[data-cy="register"]').click();

    cy.get('[data-cy="register-firstName"]')
      .find('input')
      .focus()
      .type(registerDetails["first-name"]);

    cy.get('[data-cy="register-lastName"]')
      .find('input')
      .focus()
      .type(registerDetails["last-name"]);

    cy.get('[data-cy="register-email"]')
      .find('input')
      .focus()
      .type(registerDetails["email"]);

    cy.get('[data-cy="register-password"]')
      .find('input')
      .focus()
      .type(registerDetails["password"]);

    cy.get('[data-cy="register-confirmPassword"]')
      .find('input')
      .focus()
      .type(registerDetails["password"]);

    cy.get('[data-cy="register-signUp"]').click();

    cy.url().should('include', 'localhost:3000/dashboard');

  });

  it('should sign in successfully', () => {
    cy.get('[data-cy="login"]').click();
    cy.url().should('include', 'localhost:3000/sign-in');

    cy.get('[data-cy="login-email"]')
      .find('input')
      .focus()
      .type(registerDetails["email"]);

    cy.get('[data-cy="login-password"]')
      .find('input')
      .focus()
      .type(registerDetails["password"]);

    cy.get('[data-cy="login-signIn"]').click();

    cy.url().should('include', 'localhost:3000/dashboard');

  })
})

describe('test prototype scenarios', () => {
  beforeEach(() => {
    cy.visit('localhost:3000');

    cy.fixture('api_responses/authLogin').then((response) => {
      cy.intercept('POST', '/auth/login', (req) => {
        req.reply(response);
      });
    });

    cy.fixture('api_responses/historyUnvalidated').then((response) => {
      cy.intercept('GET', '/invoice/history?is_ready=false', (req) => {
        req.reply(response)
      });
    });

    cy.fixture('api_responses/historyValidated').then((response) => {
      cy.intercept('GET', '/invoice/history?is_ready=true', (req) => {
        req.reply(response)
      });
    });

    cy.fixture('api_responses/validateBad').then((response) => {
      cy.intercept('POST', '/invoice/uploadValidate?rules=AUNZ_PEPPOL_1_0_10', (req) => {
        req.reply(response)
      });
    });

    cy.fixture('api_responses/validateBad').then((response) => {
      cy.intercept('GET', '/invoice/validate?rules=AUNZ_PEPPOL_1_0_10&id=1', (req) => {
        req.reply(response)
      });
    });

    
    cy.fixture('api_responses/validateGood').then((response) => {
      cy.intercept('GET', '/invoice/validate?rules=AUNZ_PEPPOL_1_0_10&id=2', (req) => {
        req.reply(response)
      });
    });

    cy.fixture('api_responses/sendSuccess').then((response) => {
      cy.intercept('POST', '/invoice/send_ubl', (req) => {
        req.reply(response)
      });
    });

    cy.fixture('api_responses/sendSuccess').then((response) => {
      cy.intercept('POST', '/invoice/send_ubl?xml_id=["2"]', (req) => {
        req.reply(response)
      });
    });

    cy.fixture('api_responses/createInvoicePDF').then((response) => {
      cy.intercept('POST', '/invoice/uploadCreate', (req) => {
        req.reply(response)
      });
    });

    cy.get('[data-cy="login"]').click();
    cy.url().should('include', 'localhost:3000/sign-in');

    cy.get('[data-cy="login-email"]')
      .find('input')
      .focus()
      .type(registerDetails['email']);

    cy.get('[data-cy="login-password"]')
      .find('input')
      .focus()
      .type(registerDetails['password']);

    cy.get('[data-cy="login-signIn"]').click();

    cy.url().should('include', 'localhost:3000/dashboard');
  });

  it('uploads a JSON file and sends by email', () => {

    // SENDING FILE VIA UPLOAD
    cy.get('[data-cy="dashboard-sending"]').click();

    cy.get('.css-1agvk75').selectFile(
      'cypress/fixtures/initial_files/uploadInvoice.json',
      {
        action: 'drag-drop',
      }
    );

    cy.get('[data-cy="send-email"]')
      .find('input')
      .focus()
      .type(registerDetails['email']);

    cy.get('[data-cy="send-submit"]').click();

    cy.get('[data-cy="send-confirmation').should('be.visible');
  });

  it('uploads a PDF file and sends by email', () => {

    // SENDING FILE VIA UPLOAD
    cy.get('[data-cy="dashboard-sending"]').click();

    cy.get('.css-1agvk75').selectFile(
      'cypress/fixtures/initial_files/OCRinvoice.pdf',
      {
        action: 'drag-drop',
      }
    );

    cy.get('[data-cy="send-email"]')
      .find('input')
      .focus()
      .type(registerDetails['email']);

    cy.get('[data-cy="send-submit"]').click();

    cy.get('[data-cy="send-confirmation').should('be.visible');
  });

  it('converts a PDF to XML & validates it', () => {

    // INVOICE CREATION VIA UPLOAD
    cy.get('[data-cy="dashboard-creation"]').click();

    cy.get('.css-1agvk75').selectFile(
      'cypress/fixtures/initial_files/OCRinvoice.pdf',
      {
        action: 'drag-drop',
      }
    );

    cy.get('[data-cy="generate-invoice"]').click();

    // VALIDATION FROM SELECTION
    cy.get('[data-cy="toggle-drawer"]').click();

    cy.get('[data-cy="drawer-validation"]').click();

    cy.get('[data-cy="validation-select"]')
      .parent()
      .click()
      .get('ul > li[data-value="AUNZ_PEPPOL_1_0_10"]')
      .click()
    ;
    
    cy.get('[data-cy="multiple-select"]')
      .parent()
      .click()
      .get('ul > li[data-cy="OCRinvoice.xml"]')
      .click()
    ;

    cy.get('body').click(0,0);

    cy.get('[data-cy="validation-submit"]').click();

    cy.get('[data-cy="validation-invalid"]').should('be.visible');
  });

  it('converts a JSON to XML, validates it & sends it', () => {

    // INVOICE CREATION VIA UPLOAD
    cy.get('[data-cy="dashboard-creation"]').click();

    cy.get('.css-1agvk75').selectFile(
      'cypress/fixtures/initial_files/uploadInvoice.json',
      {
        action: 'drag-drop',
      }
    );

    cy.get('[data-cy="generate-invoice"]').click();

    // VALIDATION FROM SELECTION
    cy.get('[data-cy="toggle-drawer"]').click();

    cy.get('[data-cy="drawer-validation"]').click();

    cy.get('[data-cy="multiple-select"]')
      .parent()
      .click()
      .get('ul > li[data-cy="uploadInvoice.xml"]')
      .click()
    ;

    cy.get('body').click(0,0);

    cy.get('[data-cy="validation-select"]')
      .parent()
      .click()
      .get('ul > li[data-value="AUNZ_PEPPOL_1_0_10"]')
      .click();

    cy.get('[data-cy="validation-submit"]').click();

    cy.get('[data-cy="validation-valid"]').should('be.visible');

    // SENDING FROM SELECTION
    cy.get('[data-cy="toggle-drawer"]').click();

    cy.get('[data-cy="drawer-sending"]').click();

    cy.get('[data-cy="multiple-select"]')
      .parent()
      .click()
      .get('ul > li[data-cy="uploadInvoice.xml"]')
      .click()
    ;

    cy.get('body').click(0,0);

    cy.get('[data-cy="send-email"]')
      .find('input')
      .focus()
      .type(registerDetails['email']);

    cy.get('[data-cy="send-submit"]').click();

    cy.get('[data-cy="send-confirmation').should('be.visible');
  });
});
