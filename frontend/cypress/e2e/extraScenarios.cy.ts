/// <reference types="cypress" />

const details = {
  'first-name': 'John',
  'last-name': 'Smith',
  email: 'smith@gmail.com',
  password: 'smith123',
};

describe('test user login', () => {
  beforeEach(() => {
    cy.visit('localhost:3000');

    cy.intercept('POST', '/auth/register', (req) => {
      req.reply({
        statusCode: 201,
        body: {
          message: 'User registered successfully.',
          token:
            'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImphbmUuc21pdGhAZXhhbXBsZS5jb20ifQ.hRQ0311NXzLtdBwKQk2Iqunxfy0PcVUYQ2xzF6NmfoY',
        },
      });
    });

    cy.intercept('POST', '/auth/login', (req) => {
      req.reply({
        statusCode: 200,
        body: {
          message: 'User logged in successfully.',
          token:
            'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImphbmUuc21pdGhAZXhhbXBsZS5jb20ifQ.hRQ0311NXzLtdBwKQk2Iqunxfy0PcVUYQ2xzF6NmfoY',
        },
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
      .type(details['first-name']);

    cy.get('[data-cy="register-lastName"]')
      .find('input')
      .focus()
      .type(details['last-name']);

    cy.get('[data-cy="register-email"]')
      .find('input')
      .focus()
      .type(details['email']);

    cy.get('[data-cy="register-password"]')
      .find('input')
      .focus()
      .type(details['password']);

    cy.get('[data-cy="register-confirmPassword"]')
      .find('input')
      .focus()
      .type(details['password']);

    cy.get('[data-cy="register-signUp"]').click();

    cy.url().should('include', 'localhost:3000/dashboard');
  });

  it('should sign in successfully', () => {
    cy.get('[data-cy="login"]').click();
    cy.url().should('include', 'localhost:3000/sign-in');

    cy.get('[data-cy="login-email"]')
      .find('input')
      .focus()
      .type(details['email']);

    cy.get('[data-cy="login-password"]')
      .find('input')
      .focus()
      .type(details['password']);

    cy.get('[data-cy="login-signIn"]').click();

    cy.url().should('include', 'localhost:3000/dashboard');
  });
});

describe('test prototype scenarios', () => {
  beforeEach(() => {
    cy.visit('localhost:3000');

    cy.intercept('POST', '/auth/login', (req) => {
      req.reply({
        statusCode: 200,
        body: {
          message: 'User logged in successfully.',
          token:
            'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImphbmUuc21pdGhAZXhhbXBsZS5jb20ifQ.hRQ0311NXzLtdBwKQk2Iqunxfy0PcVUYQ2xzF6NmfoY',
        },
      });
    });

    cy.get('[data-cy="login"]').click();
    cy.url().should('include', 'localhost:3000/sign-in');

    cy.get('[data-cy="login-email"]')
      .find('input')
      .focus()
      .type(details['email']);

    cy.get('[data-cy="login-password"]')
      .find('input')
      .focus()
      .type(details['password']);

    cy.get('[data-cy="login-signIn"]').click();

    cy.url().should('include', 'localhost:3000/dashboard');
  });

  it('creates an invoice via gui', () => {
    cy.get('[data-cy="invoice-creation"]').click();
    cy.get('[data-cy="create-gui"]').click();

    cy.get('[data-cy="invoice-gui-name"]')
      .find('input')
      .focus()
      .type('Test Name');

    cy.get('[data-cy="invoice-gui-number"]')
      .find('input')
      .focus()
      .type('120001');

    // Seller fields
    cy.get('[data-cy="invoice-seller-abn"]').find('input').focus().type('7766');

    cy.get('[data-cy="invoice-seller-name"]')
      .find('input')
      .focus()
      .type('Apple Incorporated');

    cy.get('[data-cy="invoice-seller-streetname"]')
      .find('input')
      .focus()
      .type('10 Adline Street');

    cy.get('[data-cy="invoice-seller-addstreetname"]')
      .find('input')
      .focus()
      .type('2 Fake St');

    cy.get('[data-cy="invoice-seller-cityname"]')
      .find('input')
      .focus()
      .type('Scanda');

    cy.get('[data-cy="invoice-seller-pc"]').find('input').focus().type('2121');

    cy.get('[data-cy="invoice-seller-country"]').type('Australia');
    cy.contains('.MuiMenuItem-root', 'Australia').click();

    // Buyer fields
    cy.get('[data-cy="invoice-buyer-abn"]').find('input').focus().type('5555');

    cy.get('[data-cy="invoice-buyer-name"]')
      .find('input')
      .focus()
      .type('Orange Porters');

    cy.get('[data-cy="invoice-buyer-streetname"]')
      .find('input')
      .focus()
      .type('21 Lone Rd');

    cy.get('[data-cy="invoice-buyer-addstreetname"]')
      .find('input')
      .focus()
      .type('19 Unknown Ave');

    cy.get('[data-cy="invoice-buyer-cityname"]')
      .find('input')
      .focus()
      .type('Andar');

    cy.get('[data-cy="invoice-buyer-pc"]').find('input').focus().type('4444');

    cy.get('[data-cy="invoice-buyer-country"]').type('Australia');
    cy.contains('.MuiMenuItem-root', 'Australia').click();
  });
});
