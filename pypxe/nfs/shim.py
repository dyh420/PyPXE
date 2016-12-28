import sys
import logging
from pypxe import helpers
import multiprocessing
import threading
import time

sys_logger = logging.getLogger('PyPXE')
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s %(message)s')
handler.setFormatter(formatter)
sys_logger.addHandler(handler)
sys_logger.setLevel(logging.INFO)

try:
        threads = []
        nfsroots = ["/home/rory/PyPXE/pypxe/nfs/nfsroot/"]

        import portmapper
        portmapper_logger = helpers.get_child_logger(sys_logger, 'NFS.PORTMAPPER')
        portmapperd = portmapper.PORTMAPPERD(logger = portmapper_logger, mode_debug = True)
        portmapperdthread = threading.Thread(target = portmapperd.listen)
        portmapperdthread.daemon = True
        portmapperdthread.start()
        threads.append(portmapperdthread)

        import mount
        mount_logger = helpers.get_child_logger(sys_logger, 'NFS.MOUNT')
        mountd = mount.MOUNTD(logger = mount_logger, mode_debug = True, nfsroots = nfsroots)
        mountdthread = threading.Thread(target = mountd.listen)
        mountdthread.daemon = True
        mountdthread.start()
        threads.append(mountdthread)

        import nfs
        nfs_logger = helpers.get_child_logger(sys_logger, 'NFS.NFS')
        nfsd = nfs.NFSD(logger = nfs_logger, mode_debug = True, nfsroots = nfsroots)
        nfsdthread = threading.Thread(target = nfsd.listen)
        nfsdthread.daemon = True
        nfsdthread.start()
        threads.append(nfsdthread)

        import lock
        lock_logger = helpers.get_child_logger(sys_logger, 'NFS.LOCK')
        lockd = lock.LOCKD(logger = lock_logger, mode_debug = True)
        lockdthread = threading.Thread(target = lockd.listen)
        lockdthread.daemon = True
        lockdthread.start()
        threads.append(lockdthread)

        while all(map(lambda x:x.isAlive(), threads)):
            time.sleep(1)
except KeyboardInterrupt:
    sys.exit('\nShutting down...')
