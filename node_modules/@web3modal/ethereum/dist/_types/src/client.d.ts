import type { Chain, Connector } from '@wagmi/core';
import { disconnect, fetchBalance, fetchEnsAvatar, fetchEnsName, getAccount, getNetwork, switchNetwork, watchAccount, watchNetwork } from '@wagmi/core';
import type { ConnectorId, ModalConnectorsOpts } from './types';
export declare class EthereumClient {
    private readonly wagmi;
    walletConnectVersion: ModalConnectorsOpts['version'];
    readonly chains: Chain[];
    constructor(wagmi: any, chains: Chain[]);
    private getWalletConnectConnectors;
    private connectWalletConnectV1;
    private connectWalletConnectV2;
    namespace: string;
    getConnectorById(id: ConnectorId | string): Connector<any, any>;
    getConnectors(): Connector<any, any>[];
    connectWalletConnect(onUri: (uri: string) => void, chainId?: number): Promise<[import("@wagmi/core").ConnectResult<import("@wagmi/core/dist/index-fc9ab085").P>, void]>;
    connectConnector(connectorId: ConnectorId | string, chainId?: number): Promise<import("@wagmi/core").ConnectResult<import("@wagmi/core/dist/index-fc9ab085").P>>;
    isInjectedProviderInstalled(): boolean;
    safeCheckInjectedProvider(providerId: string): boolean;
    getConnectedChainIds(): Promise<string[] | "ALL">;
    disconnect: typeof disconnect;
    getAccount: typeof getAccount;
    watchAccount: typeof watchAccount;
    fetchBalance: typeof fetchBalance;
    getNetwork: typeof getNetwork;
    watchNetwork: typeof watchNetwork;
    switchNetwork: typeof switchNetwork;
    fetchEnsName: typeof fetchEnsName;
    fetchEnsAvatar: typeof fetchEnsAvatar;
}
