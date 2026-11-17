import { AlertTriangle } from 'lucide-react';
import { Modal } from './Modal';
import { Button } from './Button';

interface ConfirmDialogProps {
  open: boolean;
  onClose: () => void;
  onConfirm: () => void;
  title: string;
  message: string;
  confirmLabel?: string;
  danger?: boolean;
  loading?: boolean;
}

export function ConfirmDialog({
  open,
  onClose,
  onConfirm,
  title,
  message,
  confirmLabel = 'Confirm',
  danger,
  loading,
}: ConfirmDialogProps) {
  return (
    <Modal open={open} onClose={onClose} title={title} size="sm">
      <div className="flex gap-3">
        {danger && (
          <div className="flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-[2px] border border-[#d33] bg-[#fee] text-[#d33] dark:bg-[#7f1d1d]/30">
            <AlertTriangle className="h-4 w-4" />
          </div>
        )}
        <p className="text-xs sm:text-sm text-[#202122] dark:text-[#e5e7eb] leading-relaxed">{message}</p>
      </div>
      <div className="mt-5 flex justify-end gap-2 border-t border-[#a2a9b1] dark:border-[#374151] pt-3">
        <Button variant="outline" size="sm" onClick={onClose} disabled={loading}>
          Cancel
        </Button>
        <Button variant={danger ? 'danger' : 'primary'} size="sm" onClick={onConfirm} loading={loading}>
          {confirmLabel}
        </Button>
      </div>
    </Modal>
  );
}
