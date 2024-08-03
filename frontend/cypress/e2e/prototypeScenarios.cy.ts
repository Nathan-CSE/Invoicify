/// <reference types="cypress" />


const registerDetails = {
  'first-name': 'John',
  'last-name': 'Smith',
  'email': 'smith@gmail.com',
  'password': 'smith123'
}

// describe('test user login', () => {
//   beforeEach(() => {
//     cy.visit('localhost:3000');

//     cy.intercept('POST', '/auth/register', (req) => {
//       req.reply({
//         statusCode: 201,
//         body: {
//           "message": "User registered successfully.",
//           "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImphbmUuc21pdGhAZXhhbXBsZS5jb20ifQ.hRQ0311NXzLtdBwKQk2Iqunxfy0PcVUYQ2xzF6NmfoY"
//         }
//       });
//     });

//     cy.intercept('POST', '/auth/login', (req) => {
//       req.reply({
//         statusCode: 200,
//         body: {
//           "message": "User logged in successfully.",
//           "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImphbmUuc21pdGhAZXhhbXBsZS5jb20ifQ.hRQ0311NXzLtdBwKQk2Iqunxfy0PcVUYQ2xzF6NmfoY"
//         }
//       });
//     });

//   });

//   it('should navigate to the app home screen successfully', () => {
//     cy.url().should('include', 'localhost:3000');
//   })

//   it('should navigate to the login screen successfully', () => {
//     cy.get('[data-cy="login"]').click();
//     cy.url().should('include', 'localhost:3000/sign-in');
//   })

//   it('should sign up successfully', () => {
//     cy.get('[data-cy="login"]').click();
//     cy.url().should('include', 'localhost:3000/sign-in');
//     cy.get('[data-cy="register"]').click();

//     cy.get('[data-cy="register-firstName"]')
//       .find('input')  
//       .focus()
//       .type(registerDetails["first-name"])
//     ;
    
//     cy.get('[data-cy="register-lastName"]')
//       .find('input')  
//       .focus()
//       .type(registerDetails["last-name"])
//     ;

//     cy.get('[data-cy="register-email"]')
//       .find('input')  
//       .focus()
//       .type(registerDetails["email"])
//     ;

//     cy.get('[data-cy="register-password"]')
//       .find('input')  
//       .focus()
//       .type(registerDetails["password"])
//     ;

//     cy.get('[data-cy="register-confirmPassword"]')
//       .find('input')  
//       .focus()
//       .type(registerDetails["password"])
//     ;

//     cy.get('[data-cy="register-signUp"]').click();

//     cy.url().should('include', 'localhost:3000/dashboard');

//   })

//   it('should sign in successfully', () => {
//     cy.get('[data-cy="login"]').click();
//     cy.url().should('include', 'localhost:3000/sign-in');

//     cy.get('[data-cy="login-email"]')
//       .find('input')  
//       .focus()
//       .type(registerDetails["email"])
//     ;
    
//     cy.get('[data-cy="login-password"]')
//       .find('input')  
//       .focus()
//       .type(registerDetails["password"])
//     ;

//     cy.get('[data-cy="login-signIn"]').click();

//     cy.url().should('include', 'localhost:3000/dashboard');

//   })
// })

describe('test prototype scenarios', () => {
  beforeEach(() => {
    cy.visit('localhost:3000');

    cy.intercept('POST', '/auth/login', (req) => {
      req.reply({
        statusCode: 200,
        body: {
          "message": "User logged in successfully.",
          "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImphbmUuc21pdGhAZXhhbXBsZS5jb20ifQ.hRQ0311NXzLtdBwKQk2Iqunxfy0PcVUYQ2xzF6NmfoY"
        }
      });
    });

    cy.get('[data-cy="login"]').click();
    cy.url().should('include', 'localhost:3000/sign-in');

    cy.get('[data-cy="login-email"]')
      .find('input')  
      .focus()
      .type(registerDetails["email"])
    ;
    
    cy.get('[data-cy="login-password"]')
      .find('input')  
      .focus()
      .type(registerDetails["password"])
    ;

    cy.get('[data-cy="login-signIn"]').click();

    cy.url().should('include', 'localhost:3000/dashboard');

  });

  it('uploads a JSON file and sends by email', () => {
    cy.get('[data-cy="invoice-sending"]').click();

    cy.get('.css-1agvk75').selectFile('cypress/fixtures/initial_files/uploadInvoice.json', { 
      action: 'drag-drop' 
    });

    cy.get('[data-cy="send-email"]')
      .find('input')  
      .focus()
      .type(registerDetails["email"])
    ;

    cy.get('[data-cy="send-submit"]').click();

    cy.wait(6000);

    cy.get('[data-cy="send-confirmation').should('be.visible');

  });

  it('uploads a PDF file and sends by email', () => {
    cy.get('[data-cy="invoice-sending"]').click();

    cy.get('.css-1agvk75').selectFile('cypress/fixtures/initial_files/OCRinvoice.pdf', { 
      action: 'drag-drop' 
    });

    cy.get('[data-cy="send-email"]')
      .find('input')  
      .focus()
      .type(registerDetails["email"])
    ;

    cy.get('[data-cy="send-submit"]').click();

    cy.wait(6000);

    cy.get('[data-cy="send-confirmation').should('be.visible');

  });

  it('converts a PDF file to JSON & validates it', () => {
    cy.get('[data-cy="invoice-sending"]').click();

    cy.get('.css-1agvk75').selectFile('cypress/fixtures/initial_files/OCRinvoice.pdf', { 
      action: 'drag-drop' 
    });

    cy.get('[data-cy="send-email"]')
      .find('input')  
      .focus()
      .type(registerDetails["email"])
    ;

    cy.get('[data-cy="send-submit"]').click();

    cy.wait(6000);

    cy.get('[data-cy="send-confirmation').should('be.visible');

  });

  // it('convert JSON file to XML, validate and send by email', () => {
  //   cy.get('[data-cy="invoice-creation"]').click();

  //   cy.get('.css-1agvk75').selectFile('cypress/fixtures/uploadInvoice.json', { 
  //     action: 'drag-drop' 
  //   });

  //   cy.get('[data-cy="generate-invoice"]').click();
    
  // });
})