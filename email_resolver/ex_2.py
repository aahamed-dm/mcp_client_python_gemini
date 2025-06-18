async def update_connection_service_new(connection, connection_data: ConnectionCreateSchema,
                                        db_session: AsyncSession):
    """
    Updates a connection.

    This function updates the connection with the provided data. mostly when refresh token is used.
    Args:
        connection (Connection): The connection to update.
        connection_data (ConnectionCreateSchema): The data to update the connection with.
        db_session (AsyncSession): The asynchronous database session.

    Returns:
        Connection: The updated connection.
    """
    updates_dict = connection_data.model_dump(exclude_unset=True)
    for key, value in updates_dict.items():
        setattr(connection, key, value)
    await db_session.commit()
    await db_session.refresh(connection)
    return connection
