# Bottle Email Confirmation Project

Welcome to the Bottle Email Confirmation Project! This is a simple web application built with Bottle, a micro web framework for Python, that allows users to sign up and receive a confirmation email with a link to verify their account.

## Description

The Bottle Email Confirmation Project provides a basic user authentication system with email confirmation functionality. Users can sign up for an account by providing their email address and password. Upon successful registration, a confirmation email is sent to the user's email address with a unique verification link. Users can click on the verification link to confirm their email address and activate their account.

## Features

- User Signup: Users can sign up for a new account by providing their email address and password.
- Email Confirmation: After signing up, users receive a confirmation email with a unique verification link.
- Account Activation: Users can click on the verification link in the email to confirm their email address and activate their account.
- SQLite Database: User data is stored in an SQLite database, including email addresses, hashed passwords, and verification tokens.

## Technologies Used

- Python: Used for server-side logic and backend development.
- Bottle: A micro web framework for Python used to build the web application.
- SQLite3: A lightweight relational database management system used to store user data.
- SMTP: Simple Mail Transfer Protocol used to send confirmation emails to users.

## Installation

1. Clone the repository to your local machine:
