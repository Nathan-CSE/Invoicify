/// <reference types="cypress" />

const details = {
  'first-name': 'John',
  'last-name': 'Smith',
  email: 'smith@gmail.com',
  password: 'smith123',
};

describe('user logs in and creates an xml through the creation gui', () => {
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

    cy.intercept('POST', '/invoice/create', (req) => {
      req.reply({
        statusCode: 201,
        body: {
          data: [
            {
              filename: 'mocked_filename.xml',
              invoiceId: 'mocked_invoice_id',
            },
          ],
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
    cy.get('[data-cy="dashboard-creation"]').click();
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

    // Items section
    cy.get('[data-cy="invoice-buyer-pc"]').find('input').focus().type('4444');

    cy.get('[data-cy="invoice-buyer-country"]').type('Australia');
    cy.contains('.MuiMenuItem-root', 'Australia').click();

    // We have to do this as mui is a bit funky so we first click on the element
    // And then follow it up with the actual cell data
    cy.get('.MuiDataGrid-cell').eq(1).click().type('1');
    cy.get('.MuiDataGrid-cell').eq(1).find('input').type('10');

    cy.get('.MuiDataGrid-cell').eq(2).click().type('A');
    cy.get('.MuiDataGrid-cell').eq(2).find('input').type('AAA');

    cy.get('.MuiDataGrid-cell').eq(3).click().type('A');
    cy.get('.MuiDataGrid-cell').eq(3).find('input').type('Apple');

    cy.get('.MuiDataGrid-cell').eq(4).click().type('F');
    cy.get('.MuiDataGrid-cell').eq(4).find('input').type('Fruit');

    cy.get('.MuiDataGrid-cell').eq(5).click().type('1');
    cy.get('.MuiDataGrid-cell').eq(5).find('input').type('100');

    cy.get('.MuiDataGrid-cell').eq(1).click();

    // Verification section
    cy.get('[data-cy="invoice-gui-name"]')
      .find('input')
      .should('have.value', 'Test Name');
    cy.get('[data-cy="invoice-gui-number"]')
      .find('input')
      .should('have.value', '120001');

    // Seller verification
    cy.get('[data-cy="invoice-seller-abn"]')
      .find('input')
      .should('have.value', '7766');
    cy.get('[data-cy="invoice-seller-name"]')
      .find('input')
      .should('have.value', 'Apple Incorporated');
    cy.get('[data-cy="invoice-seller-streetname"]')
      .find('input')
      .should('have.value', '10 Adline Street');
    cy.get('[data-cy="invoice-seller-addstreetname"]')
      .find('input')
      .should('have.value', '2 Fake St');
    cy.get('[data-cy="invoice-seller-cityname"]')
      .find('input')
      .should('have.value', 'Scanda');
    cy.get('[data-cy="invoice-seller-pc"]')
      .find('input')
      .should('have.value', '2121');
    cy.get('[data-cy="invoice-seller-country"]').should(
      'contain.text',
      'Australia'
    );

    // Buyer verification
    cy.get('[data-cy="invoice-buyer-abn"]')
      .find('input')
      .should('have.value', '5555');
    cy.get('[data-cy="invoice-buyer-name"]')
      .find('input')
      .should('have.value', 'Orange Porters');
    cy.get('[data-cy="invoice-buyer-streetname"]')
      .find('input')
      .should('have.value', '21 Lone Rd');
    cy.get('[data-cy="invoice-buyer-addstreetname"]')
      .find('input')
      .should('have.value', '19 Unknown Ave');
    cy.get('[data-cy="invoice-buyer-cityname"]')
      .find('input')
      .should('have.value', 'Andar');
    cy.get('[data-cy="invoice-buyer-pc"]')
      .find('input')
      .should('have.value', '4444');
    cy.get('[data-cy="invoice-buyer-country"]').should(
      'contain.text',
      'Australia'
    );

    // Check if we have navigated correctly after a successful creation
    cy.get('[data-cy="confirm-gui"]').click();
    cy.url().should('include', 'localhost:3000/invoice-creation-confirmation');
  });
});

describe('login and look at their previous invoices', () => {
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

    cy.intercept('GET', '/invoice/history', (req) => {
      req.reply({
        statusCode: 200,
        body: {
          '1': {
            id: 1,
            name: 'Invoice 1',
            completed_ubl: null,
            fields: {},
            rule: 'Rule A',
            user_id: 123,
            is_ready: false,
            is_gui: true,
          },
          '2': {
            id: 2,
            name: 'Invoice 2',
            completed_ubl: null,
            fields: {},
            rule: 'Rule B',
            user_id: 456,
            is_ready: false,
            is_gui: false,
          },
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

  it('displays all invoices correctly', () => {
    cy.get('[data-cy="dashboard-management"]').click();
    cy.wait(3000);
    cy.get('[data-cy="invoice-card"]').should('have.length', 2);
    cy.contains('[data-cy="invoice-card"]', 'Invoice 1').should('exist');
    cy.contains('[data-cy="invoice-card"]', 'Invoice 2').should('exist');
  });
});
