# Setup da VM na Azure

Especificações da máquina virtual que você precisa criar pelo **portal da Azure**
para hospedar o CTF. É uma app leve — a menor VM já dá conta.

## 1. Criar a VM

No portal Azure → **Create a resource** → **Virtual machine**:

| Configuração            | Valor recomendado                                  |
|-------------------------|----------------------------------------------------|
| Resource group          | `rg-ctf-beginner` (crie um novo)                   |
| Virtual machine name    | `vm-ctf-nimbus`                                    |
| Region                  | a mais próxima de vocês (ex: Brazil South)         |
| Image                   | **Ubuntu Server 24.04 LTS**                        |
| Size                    | **Standard B1s** (1 vCPU, 1 GB) — suficiente       |
| Authentication type     | **SSH public key**                                 |
| Username                | `azureuser`                                        |
| Public inbound ports    | **Allow selected ports** → marque **SSH (22)** e **HTTP (80)** |

> A B1s costuma estar no free tier / custa poucos centavos por hora. Se quiser
> economizar, **desligue (Stop/Deallocate)** a VM quando não estiverem jogando.

## 2. Regras de rede (NSG)

O assistente já abre 22 e 80 se você marcar as portas acima. Confirme depois em
**Networking** que existem regras de entrada permitindo:

- **22/TCP** (SSH) — idealmente restrito ao seu IP.
- **80/TCP** (HTTP) — a aplicação roda aqui. Pode deixar aberto para `Any` para
  o Carlos acessar de casa (é um ambiente descartável e intencionalmente vulnerável;
  não coloque nada real nessa VM).

## 3. Provisionar a aplicação

Conecte via SSH e rode:

```bash
ssh azureuser@<IP_PUBLICO_DA_VM>

# na VM:
sudo apt-get update -y && sudo apt-get install -y git
git clone https://github.com/wolney-fo/ctf-beginner.git
cd ctf-beginner
sudo bash setup.sh
```

O `setup.sh` instala tudo, gera as flags **aleatórias** (sem mostrar na tela),
sobe a aplicação como serviço e imprime a URL no final.

## 4. Acessar

Abra no navegador: `http://<IP_PUBLICO_DA_VM>/`

Manda esse link pro Carlos e boa caçada. 🕵️

## Comandos úteis na VM

```bash
systemctl status ctf-nimbus      # ver se está rodando
sudo systemctl restart ctf-nimbus # reiniciar (reseta cookies/sessão, não as flags)
journalctl -u ctf-nimbus -n 50   # logs, se algo der errado
```

## Reset / limpeza

- Para **regenerar as flags do zero**: rode `sudo bash setup.sh` de novo.
- Para **destruir tudo** e parar de pagar: apague o resource group `rg-ctf-beginner`
  no portal (**Delete resource group**).
