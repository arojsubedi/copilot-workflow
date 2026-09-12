# Jira example

Title: Remind readers before a book reservation expires

Readers currently receive a message when a reserved book is ready for collection, but there is no reminder before the reservation expires. Someone who misses the first message may not realize that the book is still waiting for them.

The reservation page already shows the collection deadline and whether the book has been collected. Extend the notification behavior to send one reminder on the day before that deadline, using the reader's existing notification preference.

Only active, uncollected reservations should receive a reminder. Cancelled reservations and books that have already been collected should be excluded, while the current ready-for-collection message remains unchanged.

Acceptance criteria for this fictional project's format:

- An active, uncollected reservation receives one reminder on the day before its collection deadline.
- The reminder uses the reader's current notification preference.
- Collected and cancelled reservations receive no reminder; the existing ready-for-collection message is unchanged.
