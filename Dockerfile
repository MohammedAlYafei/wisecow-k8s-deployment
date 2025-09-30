FROM ubuntu:22.04

# Install required packages including dos2unix
RUN apt-get update && \
    apt-get install -y \
    cowsay \
    fortune-mod \
    netcat-openbsd \
    dos2unix && \
    rm -rf /var/lib/apt/lists/*

# Set cowsay path
ENV PATH="/usr/games:${PATH}"

# Create working directory
WORKDIR /app

# Copy the wisecow script
COPY wisecow.sh /app/

# Fix line endings and make script executable
RUN dos2unix /app/wisecow.sh && \
    chmod +x /app/wisecow.sh

# Expose port
EXPOSE 4499

# Run the application
CMD ["./wisecow.sh"]