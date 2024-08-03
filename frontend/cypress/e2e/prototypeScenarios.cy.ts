const registerDetails = {
  'first-name': 'John',
  'last-name': 'Smith',
  'email': 'smith@gmail.com',
  'password': 'smith123'
}

describe('test user login', () => {
  beforeEach(() => {
    cy.visit('localhost:3000');

    cy.intercept('POST', '/auth/register', (req) => {
      req.reply({
        statusCode: 201,
        body: { message: 'User registered successfully' }
      });
    });

  });

  it('should navigate to the app home screen successfully', () => {
    cy.url().should('include', 'localhost:3000');
  })

  it('should navigate to the login screen successfully', () => {
    cy.get('[data-cy="login"]').click();
    cy.url().should('include', 'localhost:3000/sign-in');
  })

  it('should sign up successfully', () => {
    cy.get('[data-cy="login"]').click();
    cy.url().should('include', 'localhost:3000/sign-in');
    cy.get('[data-cy="register"]').click();

    cy.get('[data-cy="register-firstName"]')
      .find('input')  
      .focus()
      .type(registerDetails["first-name"])
    ;
    
    cy.get('[data-cy="register-lastName"]')
      .find('input')  
      .focus()
      .type(registerDetails["last-name"])
    ;

    cy.get('[data-cy="register-email"]')
      .find('input')  
      .focus()
      .type(registerDetails["email"])
    ;

    cy.get('[data-cy="register-password"]')
      .find('input')  
      .focus()
      .type(registerDetails["password"])
    ;

    cy.get('[data-cy="register-confirmPassword"]')
      .find('input')  
      .focus()
      .type(registerDetails["password"])
    ;

    cy.get('[data-cy="register-signUp"]').click();

    cy.url().should('include', 'localhost:3000/dashboard');

  })
})