import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import SignIn from '../../pages/UserAuth/SignIn';
import axios from 'axios';
import { MemoryRouter as Router } from 'react-router-dom';

describe('Signin', () => {
  //   screen.debug();

  const noop = () => {};

  it('renders the page and has the text fields', () => {
    render(
      <Router>
        <SignIn token='' setToken={noop} />
      </Router>
    );

    // screen.logTestingPlaygroundURL();
    expect(
      screen.getByRole('heading', {
        name: /sign in/i,
      })
    );

    const password = screen.getByLabelText(/password/i);
    expect(password).toBeInTheDocument();
    const email = screen.getByRole('textbox', {
      name: /email/i,
    });
    expect(email).toBeInTheDocument();
  });

  it('click on the button and registers it', async () => {
    const mockSignIn = jest.fn();
    render(
      <Router>
        <SignIn token='' setToken={noop} />
      </Router>
    );

    const SignInButton = screen.getByRole('button', {
      name: /sign in/i,
    });
    expect(SignInButton).toBeInTheDocument();
    fireEvent.click(SignInButton);
    expect(mockSignIn).toHaveBeenCalled();
  });

  //   it('shows error message when submitting with empty fields', async () => {
  //     const signInButton = screen.getByRole('button', { name: 'Sign In' });
  //     fireEvent.click(signInButton);

  //     expect(
  //       await screen.findByText('Fill out all required fields')
  //     ).toBeInTheDocument();
  //   });
});
