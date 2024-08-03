describe('test user login', () => {
  it('should navigate to the app home screen successfully', () => {
    cy.visit('localhost:3000/');
    cy.url().should('include', 'localhost:3000');
  })

  it('should navigate to the login screen successfully', () => {
    cy.visit('localhost:3000/');
    cy.get('[data-cy="login"]').click();
    cy.url().should('include', 'localhost:3000/sign-in');
  })

  it('should login successfully', () => {
    cy.visit('localhost:3000/');
    cy.get('[data-cy="login"]').click();
    cy.url().should('include', 'localhost:3000/sign-in');
  })
})