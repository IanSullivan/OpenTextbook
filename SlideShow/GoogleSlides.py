from __future__ import print_function

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def create_presentation(title):
    """
        Creates the Presentation the user has access to.
        Load pre-authorized user credentials from the environment.
        TODO(developer) - See https://developers.google.com/identity
        for guides on implementing OAuth2 for the application.
        """
    creds, _ = google.auth.default()
    # pylint: disable=maybe-no-member
    try:
        service = build('slides', 'v1', credentials=creds)

        body = {
            'title': title
        }
        presentation = service.presentations() \
            .create(body=body).execute()
        print(f"Created presentation with ID:"
              f"{(presentation.get('presentationId'))}")
        return presentation

    except HttpError as error:
        print(f"An error occurred: {error}")
        print("presentation not created")
        return error


if __name__ == '__main__':
    create_presentation("finalp")