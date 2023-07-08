import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

train_path = '//home/diogeles/intelligent_transportation_system_ModelML/runs/detect/train/results.csv'
train_path2 = '/home/diogeles/intelligent_transportation_system_ModelML/runs/detect/train2/results.csv'

df = pd.read_csv(train_path)
df2 = pd.read_csv(train_path2)
# Strip column names of whitespaces
df.columns = df.columns.str.strip()
df2.columns = df2.columns.str.strip()


# Generate a figure with matplotlib using plt.figure subplot
fig = plt.figure()

sub1 = fig.add_subplot(2, 1, 1)
sub1.set_title('Loss model YOLOv8s')
sub1.plot(df['epoch'], df['train/box_loss'], label='train/box_loss')
sub1.plot(df['epoch'], df['train/cls_loss'], label='train/cls_loss')
sub1.plot(df['epoch'], df['train/dfl_loss'], label='train/dfl_loss')

plt.xlabel('epoch')
plt.ylabel('loss')

plt.legend()

sub2 = fig.add_subplot(2, 1, 2)
sub2.set_title('Loss model YOLOv8n')
sub2.plot(df2['epoch'], df2['train/box_loss'], label='train2/box_loss')
sub2.plot(df2['epoch'], df2['train/cls_loss'], label='train2/cls_loss')
sub2.plot(df2['epoch'], df2['train/dfl_loss'], label='train2/dfl_loss')
fig.tight_layout()

# Add a legend
plt.legend()

# Save the figure
fig.savefig('train_loss.png')

fig = plt.figure()

sub1 = fig.add_subplot(2, 1, 1)
sub1.set_title('Metrics model YOLOv8s')
sub1.plot(df['epoch'], df['metrics/precision(B)'],
          label='metrics/precision(B)')
sub1.plot(df['epoch'], df['metrics/recall(B)'], label='metrics/recall(B)')
sub1.plot(df['epoch'], df['metrics/mAP50(B)'], label='metrics/mAP50(B)')
sub1.plot(df['epoch'], df['metrics/mAP50-95(B)'], label='metrics/mAP50-95(B)')

plt.xlabel('epoch')
plt.ylabel('metrics')

plt.legend()

sub2 = fig.add_subplot(2, 1, 2)
sub2.set_title('Metrics model YOLOv8n')
sub2.plot(df2['epoch'], df2['metrics/precision(B)'],
          label='metrics/precision(B)')
sub2.plot(df2['epoch'], df2['metrics/recall(B)'], label='metrics/recall(B)')
sub2.plot(df2['epoch'], df2['metrics/mAP50(B)'], label='metrics/mAP50(B)')
sub2.plot(df2['epoch'], df2['metrics/mAP50-95(B)'],
          label='metrics/mAP50-95(B)')

plt.xlabel('epoch')
plt.ylabel('metrics')

plt.legend()

fig.tight_layout()

# Add a legend
plt.legend()

# Save the figure
fig.savefig('train.png')
