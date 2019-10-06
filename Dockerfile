# Use an official Python runtime as a parent image
FROM python:3.7

RUN apt-get update

# libnss3-1d libxss1

ENV driverdir /usr/local/bin
ENV maindir /app

# Set the working directory to /app
WORKDIR ${maindir}

COPY chromedriver ${driverdir}

# Copy the current directory contents into the container at /app
COPY . ${maindir}

# Install Chrome for Selenium
RUN dpkg -i chrome.deb || apt-get install -yf
RUN apt-get install -f
RUN rm chrome.deb

RUN chmod +x ${driverdir}/chromedriver
RUN chmod 755 ${driverdir}/chromedriver

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 8000

#COPY ./chrome/ /chrome
#RUN ["c:/chrome/ChromeStandaloneSetup64.exe", "/silent", "/install"]




# Install chromedriver for Selenium

# Run app.py when the container launches
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]