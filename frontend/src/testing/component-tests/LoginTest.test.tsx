import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import SignIn from '../../pages/UserAuth/SignIn';
import axios from 'axios';
import { Router } from 'react-router-dom';

describe('Signin', () => {
  const noop = () => {};
  beforeEach(() => {
    <Router>
      render(
      <SignIn token='' setToken={noop} />
      );
    </Router>;
  });

  it('renders a login button', () => {});

  //   it('shows error message when submitting with empty fields', async () => {
  //     const signInButton = screen.getByRole('button', { name: 'Sign In' });
  //     fireEvent.click(signInButton);

  //     expect(
  //       await screen.findByText('Fill out all required fields')
  //     ).toBeInTheDocument();
  //   });
});
