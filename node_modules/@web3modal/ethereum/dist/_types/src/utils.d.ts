import type { Chain, Connector } from '@wagmi/core';
import type { ModalConnectorsOpts, WalletConnectProviderOpts } from './types';
export declare const NAMESPACE = "eip155";
export declare function w3mProvider<C extends Chain>({ projectId }: WalletConnectProviderOpts): import("@wagmi/core/dist/index-fc9ab085").C<C>;
export declare function w3mConnectors({ chains, version, projectId }: ModalConnectorsOpts): Connector<any, any>[];
