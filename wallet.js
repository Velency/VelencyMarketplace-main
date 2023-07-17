import {
  EthereumClient,
  w3mConnectors,
  w3mProvider,
  WagmiCore,
  WagmiCoreChains,
  WagmiCoreConnectors,
} from "https://unpkg.com/@web3modal/ethereum";

import { Web3Modal } from "https://unpkg.com/@web3modal/html";

// Equivalent to importing from @wagmi/core
const { configureChains, createConfig, getAccount } = WagmiCore;

// Equivalent to importing from @wagmi/core/chains
const { mainnet, bsc, polygon, avalanche, arbitrum } = WagmiCoreChains;

// Equivalent to importing from @wagmi/core/providers
const { CoinbaseWalletConnector } = WagmiCoreConnectors;

window.process = {
  env: {
    NODE_ENV: "development",
  },
};

const chains = [arbitrum, mainnet, polygon];
const projectId = "0b1e5c998294f163bf1af4d05e11e4c1";

const { publicClient } = configureChains(chains, [w3mProvider({ projectId })]);
const wagmiConfig = createConfig({
  autoConnect: true,
  connectors: w3mConnectors({ projectId, chains }),
  publicClient,
});
const ethereumClient = new EthereumClient(wagmiConfig, chains);
const web3modal = new Web3Modal({ projectId }, ethereumClient);

document.getElementById("wallet").addEventListener("click", () => {
  web3modal.openModal();
});

document.getElementById("wallet").addEventListener("click", async () => {
  try {
    const account = await getAccount();
    console.log(account);

    const csrfToken = Cookies.get("csrftoken");

    // Проверяем, подключен ли аккаунт
    if (account.isConnected) {
      const address = account.address;
      const additionalInfo = "Дополнительная информация";

      // Создаем объект с данными
      const data = { address, additionalInfo };

      // Создаем объект опций для запроса
      const options = {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrfToken, // Передаем токен CSRF в заголовке
        },
        body: JSON.stringify(data),
      };

      // Отправляем запрос на сервер Django
      const response = await fetch("/authenticate_wallet/", options);
      const json = await response.json();

      if (json.success) {
        window.location.href = "/my_profile"; // Перенаправляем на нужную страницу после успешного входа
      } else {
        console.error("Ошибка авторизации или регистрации:", json.error);
      }
    } else {
      console.error("Аккаунт не подключен.");
    }
  } catch (error) {
    console.error("Ошибка авторизации через WalletConnect:", error);
  }
});
