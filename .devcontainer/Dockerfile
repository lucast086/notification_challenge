FROM python:3.13-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/workspace

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    zsh \
    git \
    sudo \
    gnupg \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID
    
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME -s /bin/zsh \
    && apt-get update \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME \
    && rm -rf /var/lib/apt/lists/*
    

USER $USERNAME

RUN sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended
ENV SHELL=/bin/zsh

RUN curl -sSL https://install.python-poetry.org | python3 - \
    && echo 'export PATH="/home/$USERNAME/.local/bin:$PATH"' >> /home/$USERNAME/.bashrc \
    && echo 'export PATH="/home/$USERNAME/.local/bin:$PATH"' >> /home/$USERNAME/.zshrc

ENV POETRY_NO_INTERACTION=1 \                                                                                                                                                               
    POETRY_VIRTUALENVS_CREATE=true \                                                                                                                                                        
    POETRY_VIRTUALENVS_IN_PROJECT=true \                                                                                                                                                    
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /workspace

CMD ["/bin/zsh"]