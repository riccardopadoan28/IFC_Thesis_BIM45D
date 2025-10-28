import { Viewer } from '@xeokit/xeokit-sdk';

declare interface Viewers {
    [key: string]: Viewer;
}

export declare class XeoViewerService {
    static instance: XeoViewerService;
    _viewers: Viewers;
    constructor();
    static getInstance(): XeoViewerService;
    setViewer(viewer: Viewer, id: string): void;
    getViewer(id: string): Viewer | null;
}

export { }
